"""Main window — form, embedded WebView, progress bar, log output."""

import shutil
from pathlib import Path

from PySide6.QtCore import (
    Qt,
    QEventLoop,
    QRect,
    QTimer,
    QUrl,
    Signal,
    Slot,
)
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QProgressBar,
    QPushButton,
    QVBoxLayout,
    QWidget,
    QSizePolicy,
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage

from yuketang_downloader.utils.paths import get_browser_cache_dir
from yuketang_downloader.core.pdf_builder import build_pdf


# ======================================================================
#  JavaScript snippets (same selectors as the original Playwright script)
# ======================================================================

_JS_CLICK_THUMBNAIL = """
(function() {
    try {
        var thumbs = document.querySelectorAll('.thumbImg-container');
        if (thumbs.length <= %d) return JSON.stringify({ok:false,reason:'idx out of range'});
        var t = thumbs[%d];
        t.scrollIntoView({behavior:'instant',block:'nearest'});
        try { t.click(); } catch(e) {}
        t.dispatchEvent(new MouseEvent('click',{bubbles:true,cancelable:true,view:window}));
        return JSON.stringify({ok:true});
    } catch(e) {
        return JSON.stringify({ok:false,reason:e.toString()});
    }
})()
"""

_JS_REMOVE_OVERLAY = """
(function() {
    try {
        var el = document.querySelector(
            '#app > div.viewContainer > div > section > main > div '
            + '> div.basePPTMain.basePPTInline > div > div.layout_body '
            + '> div.layout_right_switch'
        );
        if (el) { el.remove(); }
        return JSON.stringify({ok:true});
    } catch(e) { return JSON.stringify({ok:false}); }
})()
"""

_JS_GET_SLIDE_RECT = """
(function() {
    try {
        window.scrollTo(0, 0);
        var el = document.querySelector('.slide_layer');
        if (!el) return JSON.stringify({ok:false,reason:'no .slide_layer'});
        var r = el.getBoundingClientRect();
        return JSON.stringify({ok:true, x:r.left, y:r.top, w:r.width, h:r.height});
    } catch(e) { return JSON.stringify({ok:false,reason:e.toString()}); }
})()
"""

_JS_COUNT_THUMBNAILS = """
(function() {
    var thumbs = document.querySelectorAll('.thumbImg-container');
    return thumbs.length;
})()
"""


class MainWindow(QMainWindow):
    """Main application window with embedded browser."""

    MIN_WIDTH = 900
    MIN_HEIGHT = 650

    def __init__(self, config, settings_path, profile):
        super().__init__()
        self._config = config
        self._settings_path = settings_path

        self.setWindowTitle("🚀 雨课堂下载器 (内嵌浏览器版)")
        self.setMinimumSize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # ---- central widget + root layout ----
        central = QWidget()
        self.setCentralWidget(central)
        root = QVBoxLayout(central)
        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(8)

        # ================================================================
        #  Row: Form fields
        # ================================================================
        form = QFormLayout()
        form.setSpacing(6)

        # URL
        url_row = QHBoxLayout()
        self._url_edit = QLineEdit()
        self._url_edit.setPlaceholderText("https://changjiang.yuketang.cn/...")
        url_row.addWidget(self._url_edit, 1)
        self._start_btn = QPushButton("▶ 开始下载")
        self._start_btn.setFixedWidth(110)
        self._start_btn.clicked.connect(self._on_start)
        url_row.addWidget(self._start_btn)
        self._cancel_btn = QPushButton("⏹ 取消")
        self._cancel_btn.setFixedWidth(80)
        self._cancel_btn.setEnabled(False)
        self._cancel_btn.clicked.connect(self._on_cancel)
        url_row.addWidget(self._cancel_btn)
        form.addRow("课件网址:", url_row)

        # Save dir
        dir_row = QHBoxLayout()
        self._dir_edit = QLineEdit()
        dir_row.addWidget(self._dir_edit, 1)
        browse_btn = QPushButton("浏览…")
        browse_btn.setFixedWidth(80)
        browse_btn.clicked.connect(self._browse_dir)
        dir_row.addWidget(browse_btn)
        form.addRow("截图暂存目录:", dir_row)

        # PDF name
        self._pdf_edit = QLineEdit()
        form.addRow("输出 PDF 文件名:", self._pdf_edit)

        root.addLayout(form)

        # ================================================================
        #  Status + progress
        # ================================================================
        status_row = QHBoxLayout()
        self._status_label = QLabel("就绪 — 输入网址后点击「开始下载」")
        self._status_label.setStyleSheet("color: #666;")
        status_row.addWidget(self._status_label, 1)

        self._progress_bar = QProgressBar()
        self._progress_bar.setFixedWidth(200)
        self._progress_bar.setVisible(False)
        status_row.addWidget(self._progress_bar)
        root.addLayout(status_row)

        # ================================================================
        #  QWebEngineView — embedded browser
        # ================================================================
        self._web_view = QWebEngineView()
        self._web_view.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding
        )
        self._web_page = QWebEnginePage(profile, self._web_view)
        self._web_view.setPage(self._web_page)
        # Enable DevTools for debugging (right-click → Inspect)
        self._web_view.page().setInspectedPage(
            QWebEnginePage(self._web_view)
        )
        root.addWidget(self._web_view, 1)

        # ================================================================
        #  Log area
        # ================================================================
        self._log_area = QPlainTextEdit()
        self._log_area.setReadOnly(True)
        self._log_area.setMaximumBlockCount(500)
        log_font = QFont("Menlo", 10)
        self._log_area.setFont(log_font)
        self._log_area.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: none;
            }
        """)
        self._log_area.setFixedHeight(160)
        root.addWidget(self._log_area)

        # ================================================================
        #  State
        # ================================================================
        self._login_timer = QTimer(self)
        self._login_timer.setInterval(1000)
        self._login_timer.timeout.connect(self._poll_thumbnails)

        self._worker = None
        self._worker_thread = None
        self._image_paths: list[str] = []
        self._total_slides = 0

        # ---- restore saved values ----
        if self._config.last_url:
            self._url_edit.setText(self._config.last_url)
        if self._config.last_save_dir:
            self._dir_edit.setText(self._config.last_save_dir)
        else:
            self._dir_edit.setText(str(Path.home() / "Downloads" / "yuketang_temp"))
        if self._config.last_output_name:
            self._pdf_edit.setText(self._config.last_output_name)
        else:
            self._pdf_edit.setText("courseware.pdf")

        # ---- restore window geometry ----
        if self._config.window_geometry:
            try:
                # geometry string format: "WxH+X+Y"
                parts = self._config.window_geometry.replace("x", " ").replace("+", " ").split()
                # The old tkinter geometry format is different — skip for now
                pass
            except Exception:
                pass

    # ================================================================
    #  Form actions
    # ================================================================

    def _browse_dir(self):
        path = QFileDialog.getExistingDirectory(self, "选择截图暂存目录")
        if path:
            self._dir_edit.setText(path)

    def _on_start(self):
        url = self._url_edit.text().strip()
        if not url:
            QMessageBox.warning(self, "输入错误", "课件网址不能为空。")
            return

        save_dir = self._dir_edit.text().strip()
        if not save_dir:
            save_dir = str(Path.home() / "Downloads" / "yuketang_temp")

        output_pdf = self._pdf_edit.text().strip()
        if not output_pdf:
            output_pdf = "courseware.pdf"
        if not output_pdf.endswith(".pdf"):
            output_pdf += ".pdf"

        # Ensure PDF path is absolute (app bundle is read-only)
        pdf_path = Path(output_pdf)
        if not pdf_path.is_absolute():
            pdf_path = Path.home() / "Downloads" / pdf_path
        output_pdf = str(pdf_path)

        # Persist
        self._config.last_url = url
        self._config.last_save_dir = save_dir
        self._config.last_output_name = output_pdf
        self._config.save(self._settings_path)

        # Switch to running state
        self._set_running(True)
        self._log_area.clear()
        self._progress_bar.setVisible(True)
        self._progress_bar.setValue(0)
        self._image_paths = []
        self._total_slides = 0

        self._log("📡 正在加载课件页面…")
        self._status_label.setText("正在加载页面…")

        # Ensure save dir
        Path(save_dir).mkdir(parents=True, exist_ok=True)

        # Start worker thread
        self._start_worker(url, save_dir, output_pdf)

    def _on_cancel(self):
        if self._worker:
            self._worker.cancel()
            self._log("⏸ 正在取消…（完成当前页后停止）")
            self._cancel_btn.setEnabled(False)

    # ================================================================
    #  Worker management
    # ================================================================

    def _start_worker(self, url, save_dir, output_pdf):
        from yuketang_downloader_embedded.core.worker import DownloadWorker
        from PySide6.QtCore import QThread

        self._worker_thread = QThread(self)
        self._worker = DownloadWorker(url, save_dir, output_pdf)
        self._worker.moveToThread(self._worker_thread)

        # UI update signals (worker → main)
        self._worker.sig_status.connect(self._on_status)
        self._worker.sig_progress.connect(self._on_progress)
        self._worker.sig_log.connect(self._log)
        self._worker.sig_error.connect(self._on_error)
        self._worker.sig_done.connect(self._on_done)

        # Browser-command signals (worker → main)
        self._worker.sig_navigate.connect(self._on_navigate)
        self._worker.sig_wait_login.connect(self._on_wait_login)
        self._worker.sig_capture.connect(self._on_capture)
        self._worker.sig_build_pdf.connect(self._on_build_pdf)

        # Worker done → clean up thread
        self._worker_thread.started.connect(self._worker.run)
        self._worker_thread.finished.connect(self._on_thread_finished)
        self._worker_thread.finished.connect(
            self._worker_thread.deleteLater
        )

        self._worker_thread.start()

    def _on_thread_finished(self):
        self._worker = None
        self._worker_thread = None

    # ================================================================
    #  UI update slots (worker → main)
    # ================================================================

    @Slot(str)
    def _on_status(self, msg):
        self._status_label.setText(msg)

    @Slot(int, int)
    def _on_progress(self, current, total):
        if total > 0:
            self._progress_bar.setMaximum(total)
            self._progress_bar.setValue(current)
        self._status_label.setText(f"📸 正在截取第 {max(1, current)}/{total} 页…")

    @Slot(str)
    def _log(self, msg):
        self._log_area.appendPlainText(msg)

    @Slot(str)
    def _on_error(self, msg):
        self._log(f"❌ 错误: {msg}")
        QMessageBox.critical(self, "下载失败", msg)
        self._set_running(False)

    @Slot(str)
    def _on_done(self, path):
        self._progress_bar.setValue(self._progress_bar.maximum())
        self._status_label.setText("✅ 下载完成！")
        self._log(f"📦 PDF 已保存到: {path}")
        QMessageBox.information(self, "下载完成", f"课件 PDF 已生成：\n\n{path}")
        self._set_running(False)

    # ================================================================
    #  Browser-command slots (worker → main, executed on main thread)
    # ================================================================

    @Slot(str)
    def _on_navigate(self, url):
        """Load the course URL in the embedded browser."""
        self._web_view.load(QUrl(url))

        # Wait for page to finish loading, then tell worker
        def on_load_finished(ok):
            self._web_view.page().loadFinished.disconnect(on_load_finished)
            if self._worker:
                self._worker.navigate_result(ok)

        self._web_view.page().loadFinished.connect(on_load_finished)

    @Slot()
    def _on_wait_login(self):
        """Start polling for .thumbImg-container."""
        self._log("⏳ 请在内嵌浏览器中扫码登录…")
        self._log("    （页面加载较慢属正常现象，最长等待 10 分钟）")
        self._login_deadline = 0
        self._login_timer.start()
        # Set a 10-minute timeout (plenty of time for page load + QR scan)
        QTimer.singleShot(600_000, self._login_timeout)

        def on_poll():
            self._web_view.page().runJavaScript(
                _JS_COUNT_THUMBNAILS, self._on_login_check
            )

        # Replace timer callback
        self._login_timer.timeout.disconnect()
        self._login_timer.timeout.connect(on_poll)

    def _on_login_check(self, count):
        """JS callback: check how many thumbnails exist."""
        if count is not None and count > 0:
            self._login_timer.stop()
            self._total_slides = int(count)
            self._log(f"✅ 检测到 {self._total_slides} 页课件")
            if self._worker:
                self._worker.login_result(self._total_slides)

    def _login_timeout(self):
        """120-second deadline reached."""
        if self._login_timer.isActive():
            self._login_timer.stop()
            self._log("❌ 超时：未能检测到课件页面，请确认已登录或网址正确。")
            if self._worker:
                self._worker.cancel()

    @Slot(int)
    def _on_capture(self, slide_index):
        """Initiate the screenshot chain for one slide — all inline."""
        self._cap_idx = slide_index
        self._cap_save = Path(self._dir_edit.text().strip())

        # Safety timer: if anything hangs, abort after 15 s
        self._cap_safety = QTimer(self)
        self._cap_safety.setSingleShot(True)
        self._cap_safety.timeout.connect(self._cap_abort)
        self._cap_safety.start(15_000)

        self._log(f"  → 点击缩略图 #{slide_index + 1}…")
        js = _JS_CLICK_THUMBNAIL % (slide_index, slide_index)
        self._web_view.page().runJavaScript(js, self._cap_on_clicked)

    def _cap_abort(self):
        self._log(f"  └ 截图超时，跳过第 {self._cap_idx + 1} 页")
        if self._worker:
            self._worker.capture_result("", False)

    def _cap_on_clicked(self, raw):
        self._log(f"  └ 点击回调: {raw}")
        # Wait 4 s for slide render
        QTimer.singleShot(4000, self._cap_remove_overlay)

    def _cap_remove_overlay(self):
        js = _JS_REMOVE_OVERLAY
        self._web_view.page().runJavaScript(js, self._cap_get_rect)

    def _cap_get_rect(self, _raw):
        js = _JS_GET_SLIDE_RECT
        self._web_view.page().runJavaScript(js, self._cap_grab)

    def _cap_grab(self, raw):
        self._cap_safety.stop()

        import json
        try:
            rect = json.loads(raw) if isinstance(raw, str) else raw
        except (json.JSONDecodeError, TypeError):
            rect = None

        if not rect:
            self._log(f"  └ slide_layer 未找到 (raw={raw})")
            if self._worker:
                self._worker.capture_result("", False)
            return

        from PySide6.QtGui import QPixmap

        view = self._web_view
        ratio = view.devicePixelRatio()

        # Use render() to force synchronous paint (grab() fails on GPU-accelerated WebEngine)
        full_pm = QPixmap(view.size() * ratio)
        full_pm.setDevicePixelRatio(ratio)
        view.render(full_pm)

        # getBoundingClientRect returns CSS pixels → convert to device pixels
        x = int(rect.get("x", 0) * ratio)
        y = int(rect.get("y", 0) * ratio)
        w = int(rect.get("w", 0) * ratio)
        h = int(rect.get("h", 0) * ratio)

        if w <= 0 or h <= 0:
            self._log(f"  └ 尺寸无效: {w}x{h}")
            if self._worker:
                self._worker.capture_result("", False)
            return

        target = QRect(x, y, w, h)
        clipped = target.intersected(full_pm.rect())
        if clipped.isEmpty():
            self._log(f"  └ 坐标 ({x},{y} {w}x{h}) 超出可视区")
            if self._worker:
                self._worker.capture_result("", False)
            return

        slide_pm = full_pm.copy(clipped)
        path = str(self._cap_save / f"page_{self._cap_idx + 1:03d}.png")
        ok = slide_pm.save(path, "PNG")
        if ok:
            self._image_paths.append(path)
            self._log(f"  └ ✓ page_{self._cap_idx + 1:03d}.png ({clipped.width()}x{clipped.height()})")
        else:
            self._log(f"  └ PNG 保存失败: {path}")
        self._log(f"  └ 通知 worker…")
        if self._worker:
            self._worker.capture_result(path, ok)
            self._log(f"  └ 通知完成")

    @Slot(list, str)
    def _on_build_pdf(self, image_paths, output_path):
        """Build the final PDF."""
        try:
            self._log(f"📦 正在合成 {len(image_paths)} 张图片为 PDF…")
            build_pdf(image_paths, output_path)
            self._log("✅ PDF 合成完成")

            # Clean up temp images
            save_dir = self._dir_edit.text().strip()
            try:
                shutil.rmtree(save_dir)
                self._log("🧹 临时文件已清理")
            except OSError:
                pass

            if self._worker:
                self._worker.build_result(output_path)
        except Exception as exc:
            self._log(f"❌ PDF 合成失败: {exc}")
            if self._worker:
                self._worker.build_result("")

    # ================================================================
    #  Login polling (original timer, restored when not in worker mode)
    # ================================================================

    def _poll_thumbnails(self):
        """Fallback polling method."""
        self._web_view.page().runJavaScript(
            _JS_COUNT_THUMBNAILS, self._on_login_check
        )

    # ================================================================
    #  UI helpers
    # ================================================================

    def _set_running(self, running):
        state = not running  # True = enabled when NOT running
        self._url_edit.setEnabled(state)
        self._dir_edit.setEnabled(state)
        self._pdf_edit.setEnabled(state)
        self._start_btn.setEnabled(state)
        self._cancel_btn.setEnabled(running)
        if not running:
            self._progress_bar.setVisible(False)

    def closeEvent(self, event):
        # Cancel any running worker
        if self._worker:
            self._worker.cancel()
        if self._worker_thread and self._worker_thread.isRunning():
            self._worker_thread.quit()
            self._worker_thread.wait(5000)

        # Persist config
        self._config.window_geometry = ""
        self._config.save(self._settings_path)
        super().closeEvent(event)
