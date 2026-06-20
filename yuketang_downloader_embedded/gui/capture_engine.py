"""CaptureStateMachine — chains async JS calls on the main thread to
screenshot exactly one slide from the embedded QWebEngineView.

Key design points:
- A safety timeout (15 s) ensures we never hang forever.
- All JS snippets are wrapped in try/catch so callbacks are guaranteed.
- The click uses dispatchEvent(MouseEvent) for better compatibility.
"""

import json
from pathlib import Path

from PySide6.QtCore import (
    QObject,
    QRect,
    QTimer,
    Signal,
)
from PySide6.QtWebEngineCore import QWebEnginePage


# -------------------------------------------------------------------
#  JavaScript snippets — every one wraps in try/catch
# -------------------------------------------------------------------

_JS_CLICK = """
(function() {
    try {
        var thumbs = document.querySelectorAll('.thumbImg-container');
        if (thumbs.length <= %(idx)d) return JSON.stringify({ok: false, reason: 'thumbnail ' + %(idx)d + ' not found (total ' + thumbs.length + ')'});
        var t = thumbs[%(idx)d];
        t.scrollIntoView({behavior: 'instant', block: 'nearest'});
        // Use MouseEvent dispatch for better compatibility than .click()
        t.dispatchEvent(new MouseEvent('click', {bubbles: true, cancelable: true, view: window}));
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, reason: e.toString()});
    }
})()
"""

_JS_REMOVE = """
(function() {
    try {
        var el = document.querySelector(
            '#app > div.viewContainer > div > section > main > div '
            + '> div.basePPTMain.basePPTInline > div > div.layout_body '
            + '> div.layout_right_switch'
        );
        if (el) { el.remove(); }
        return JSON.stringify({ok: true});
    } catch(e) {
        return JSON.stringify({ok: false, reason: e.toString()});
    }
})()
"""

_JS_RECT = """
(function() {
    try {
        window.scrollTo(0, 0);
        var el = document.querySelector('.slide_layer');
        if (!el) return JSON.stringify({ok: false, reason: 'no .slide_layer element'});
        var r = el.getBoundingClientRect();
        return JSON.stringify({ok: true, x: r.left, y: r.top, w: r.width, h: r.height});
    } catch(e) {
        return JSON.stringify({ok: false, reason: e.toString()});
    }
})()
"""


def _parse(raw):
    """Safely parse the JS return value into a dict."""
    try:
        return json.loads(raw) if isinstance(raw, str) else raw
    except (json.JSONDecodeError, TypeError):
        return None


class CaptureStateMachine(QObject):
    """Drives the async capture sequence for one slide."""

    sig_finished = Signal(str, bool)  # image_path, success
    sig_log = Signal(str)             # debug messages

    _SAFETY_MS = 15_000  # never wait longer than this for ANY step

    def __init__(self, page: QWebEnginePage, slide_index: int, save_dir: Path):
        super().__init__()
        self._page = page
        self._idx = slide_index
        self._save_dir = save_dir
        self._safety_timer = QTimer(self)
        self._safety_timer.setSingleShot(True)
        self._safety_timer.timeout.connect(self._abort)

    # ------------------------------------------------------------------
    #  Public entry point
    # ------------------------------------------------------------------

    def start(self) -> None:
        self._safety_timer.start(self._SAFETY_MS)
        js = _JS_CLICK % {"idx": self._idx}
        self._page.runJavaScript(js, self._on_clicked)

    # ------------------------------------------------------------------
    #  Abort
    # ------------------------------------------------------------------

    def _abort(self) -> None:
        self.sig_log.emit(f"  └ 截图超时 (>{self._SAFETY_MS // 1000}s)，跳过第 {self._idx + 1} 页")
        self.sig_finished.emit("", False)

    # ------------------------------------------------------------------
    #  Step callbacks
    # ------------------------------------------------------------------

    def _on_clicked(self, raw) -> None:
        result = _parse(raw)
        if not result or not result.get("ok"):
            reason = result.get("reason", "unknown") if result else "no response"
            self.sig_log.emit(f"  └ 点击缩略图 #{self._idx + 1} 失败: {reason}")
            self._safety_timer.stop()
            self.sig_finished.emit("", False)
            return
        # 4-second render wait (was 2s, increased for slow connections)
        QTimer.singleShot(4000, self._remove_overlay)

    def _remove_overlay(self) -> None:
        self._page.runJavaScript(_JS_REMOVE, self._on_overlay_gone)

    def _on_overlay_gone(self, _raw) -> None:
        self._page.runJavaScript(_JS_RECT, self._on_rect)

    def _on_rect(self, raw) -> None:
        self._safety_timer.stop()
        rect = _parse(raw)

        if not rect or not rect.get("ok"):
            reason = rect.get("reason", "unknown") if rect else "no response"
            self.sig_log.emit(f"  └ .slide_layer 获取失败: {reason}")
            self.sig_finished.emit("", False)
            return

        view = self._page.view()
        if view is None:
            self.sig_log.emit("  └ QWebEngineView 不存在")
            self.sig_finished.emit("", False)
            return

        # Grab full visible area, then crop
        full_pm = view.grab()
        x = int(rect.get("x", 0))
        y = int(rect.get("y", 0))
        w = int(rect.get("w", 0))
        h = int(rect.get("h", 0))

        if w <= 0 or h <= 0:
            self.sig_log.emit(f"  └ slide 尺寸异常: {w}x{h}")
            self.sig_finished.emit("", False)
            return

        target = QRect(x, y, w, h)
        clipped = target.intersected(full_pm.rect())
        if clipped.isEmpty():
            self.sig_log.emit(f"  └ slide 区域 ({x},{y} {w}x{h}) 不在可视区")
            self.sig_finished.emit("", False)
            return

        slide_pm = full_pm.copy(clipped)
        path = str(self._save_dir / f"page_{self._idx + 1:03d}.png")
        ok = slide_pm.save(path, "PNG")
        if ok:
            self.sig_log.emit(f"  └ page_{self._idx + 1:03d}.png ({clipped.width()}x{clipped.height()})")
        else:
            self.sig_log.emit(f"  └ PNG 写入失败: {path}")
        self.sig_finished.emit(path, ok)
