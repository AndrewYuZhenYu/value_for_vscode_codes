"""Root application window — macOS GUI for the Rain Classroom Downloader."""

import tkinter as tk
from pathlib import Path

from yuketang_downloader.utils.paths import (
    get_app_support_dir,
    get_settings_path,
    get_browser_cache_dir,
)
from yuketang_downloader.utils.config import AppConfig
from yuketang_downloader.gui.main_window import MainWindow


class YuketangApp(tk.Tk):
    """Root Tk window for the Rain Classroom Downloader GUI."""

    APP_NAME = "Rain Classroom Downloader"
    MIN_WIDTH = 680
    MIN_HEIGHT = 540

    def __init__(self):
        super().__init__()

        self.title(self.APP_NAME)
        self.minsize(self.MIN_WIDTH, self.MIN_HEIGHT)

        # Ensure Application Support directory exists
        app_support = get_app_support_dir()
        app_support.mkdir(parents=True, exist_ok=True)

        # Load persisted settings
        self._settings_path = get_settings_path()
        self._config = AppConfig.load(self._settings_path)

        # Pre-launch environment checks
        if not self._check_playwright_browsers():
            self._show_browser_missing_dialog()
            return

        # Build the main UI
        self._main_window = MainWindow(self, self._config, self._settings_path)
        self._main_window.pack(fill="both", expand=True)

        # Restore saved window geometry
        if self._config.window_geometry:
            try:
                self.geometry(self._config.window_geometry)
            except tk.TclError:
                pass

        # Persist geometry on close
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Bring to front
        self.lift()
        self.focus_force()

    # ---- private helpers ----

    def _check_playwright_browsers(self) -> bool:
        """Return True if Playwright's Chromium is available."""
        # 方法 1: 直接用磁盘路径查找（可靠，不依赖 Playwright 内部 API）
        for base in (
            Path.home() / "Library" / "Caches" / "ms-playwright",
            Path.home() / ".cache" / "ms-playwright",
        ):
            if base.exists():
                for d in base.iterdir():
                    if d.is_dir() and d.name.startswith("chromium"):
                        # macOS arm64 → chrome-mac-arm64; x86_64 → chrome-mac
                        for sub in (d / "chrome-mac-arm64", d / "chrome-mac"):
                            if any(
                                (sub / name).exists()
                                for name in (
                                    "Google Chrome for Testing.app",
                                    "Chromium.app",
                                    "Chromium",
                                )
                            ):
                                return True

        # 方法 2: 用 Playwright API 查找（打包环境下可能失效）
        try:
            from playwright.sync_api import sync_playwright

            pw = sync_playwright().start()
            try:
                path = pw.chromium.executable_path
                if path and Path(path).exists():
                    return True
            finally:
                pw.stop()
        except Exception:
            pass

        return False

    def _show_browser_missing_dialog(self) -> None:
        """Block the UI with a dialog explaining how to install Chromium."""
        import tkinter.messagebox as mb

        self.withdraw()  # hide empty root window
        mb.showwarning(
            title="Chromium Not Found",
            message=(
                "The Chromium browser required by Playwright was not found.\n\n"
                "Please run these commands in Terminal:\n\n"
                "    pip install playwright\n"
                "    playwright install chromium\n\n"
                "Then restart this application."
            ),
        )
        self.destroy()

    def _on_close(self) -> None:
        """Persist settings and tear down the application."""
        self._config.window_geometry = self.geometry()
        self._config.save(self._settings_path)
        self.destroy()
