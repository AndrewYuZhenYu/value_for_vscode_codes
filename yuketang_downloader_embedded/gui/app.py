"""Root QApplication — macOS GUI for the embedded-browser edition."""

import sys
from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWebEngineCore import QWebEngineProfile

from yuketang_downloader.utils.paths import (
    get_app_support_dir,
    get_settings_path,
    get_browser_cache_dir,
)
from yuketang_downloader.utils.config import AppConfig
from yuketang_downloader_embedded.gui.main_window import MainWindow


class EmbeddedYuketangApp(QApplication):
    """Qt application for the embedded-browser Rain Classroom Downloader."""

    APP_NAME = "Rain Classroom Downloader (Embedded)"

    def __init__(self, argv):
        super().__init__(argv)

        self.setApplicationName(self.APP_NAME)
        self.setOrganizationName("AndrewYu")
        self.setApplicationDisplayName("雨课堂下载器 (内嵌版)")

        # Ensure Application Support directory exists
        app_support = get_app_support_dir()
        app_support.mkdir(parents=True, exist_ok=True)

        # Load persisted settings
        self._settings_path = get_settings_path()
        self._config = AppConfig.load(self._settings_path)

        # Pre-launch check: can we import WebEngine?
        if not self._check_webengine():
            return

        # Create persistent browser profile (stores cookies for auto-login)
        browser_cache = str(get_browser_cache_dir())
        self._profile = QWebEngineProfile("rain_classroom", self)
        self._profile.setPersistentStoragePath(browser_cache)
        self._profile.setHttpCacheType(
            QWebEngineProfile.HttpCacheType.DiskHttpCache
        )

        # Build the main window
        self._main_window = MainWindow(
            self._config, self._settings_path, self._profile
        )
        self._main_window.show()

    def _check_webengine(self) -> bool:
        """Return True if QtWebEngine is available."""
        try:
            from PySide6.QtWebEngineWidgets import QWebEngineView  # noqa: F811
            return True
        except ImportError:
            from PySide6.QtWidgets import QMessageBox

            QMessageBox.critical(
                None,
                "组件缺失",
                "Qt WebEngine 组件未找到。\n\n"
                "请运行以下命令安装：\n"
                "    pip install PySide6\n\n"
                "PySide6 已包含 QtWebEngine 模块。",
            )
            return False
