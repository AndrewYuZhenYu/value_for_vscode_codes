"""DownloadWorker — orchestrates the download on a QThread.

Uses plain Python threading primitives (threading.Event) for cross-thread
signaling — NOT QEventLoop, which has proven unreliable for this pattern.
"""

import threading

from PySide6.QtCore import (
    QObject,
    QThread,
    Signal,
    Slot,
)


class DownloadWorker(QObject):
    """QObject that lives on a QThread, orchestrating the download.

    Cross-thread communication:
      Worker → Main:  Qt signals (sig_navigate, sig_capture, ...)
      Main → Worker:  threading.Event + result attributes
                      (set by main thread in capture callbacks,
                       waited on by worker with .wait())
    """

    # ---- UI-update signals ----
    sig_status = Signal(str)
    sig_progress = Signal(int, int)
    sig_log = Signal(str)
    sig_error = Signal(str)
    sig_done = Signal(str)

    # ---- Browser-command signals (worker → main) ----
    sig_navigate = Signal(str)
    sig_wait_login = Signal()
    sig_capture = Signal(int)
    sig_build_pdf = Signal(list, str)

    def __init__(self, course_url, save_dir, output_pdf):
        super().__init__()
        self._course_url = course_url
        self._save_dir = save_dir
        self._output_pdf = output_pdf
        self._cancel_flag = False

        # ---- Cross-thread result passing via threading.Event ----
        self._navigate_event = threading.Event()
        self._navigate_ok = False

        self._login_event = threading.Event()
        self._login_count = 0

        self._capture_event = threading.Event()
        self._capture_path = ""
        self._capture_ok = False

        self._build_event = threading.Event()
        self._build_result_path = ""

    # ------------------------------------------------------------------
    #  Public API (called from main thread to pass results back)
    # ------------------------------------------------------------------

    def navigate_result(self, ok: bool) -> None:
        self._navigate_ok = ok
        self._navigate_event.set()

    def login_result(self, count: int) -> None:
        self._login_count = count
        self._login_event.set()

    def capture_result(self, path: str, ok: bool) -> None:
        self._capture_path = path
        self._capture_ok = ok
        self._capture_event.set()

    def build_result(self, path: str) -> None:
        self._build_result_path = path
        self._build_event.set()

    # ------------------------------------------------------------------
    #  Control
    # ------------------------------------------------------------------

    @Slot()
    def run(self) -> None:
        """Main entry point — called when the QThread starts."""
        try:
            self._do_download()
        except Exception as exc:
            self.sig_error.emit(f"Unexpected error: {exc}")

    def cancel(self) -> None:
        self._cancel_flag = True
        # Wake up any blocked wait so the worker can exit cleanly
        self._navigate_event.set()
        self._login_event.set()
        self._capture_event.set()
        self._build_event.set()

    # ------------------------------------------------------------------
    #  Orchestration
    # ------------------------------------------------------------------

    def _do_download(self) -> None:
        # ---- navigate ----
        self.sig_status.emit("Loading page…")
        self.sig_log.emit(f"Navigating to: {self._course_url}")
        self._navigate_event.clear()
        self.sig_navigate.emit(self._course_url)

        if not self._navigate_event.wait(timeout=60):
            self.sig_error.emit("Page load timeout.")
            return
        if self._cancel_flag:
            return
        if not self._navigate_ok:
            self.sig_error.emit("Failed to load the course page.")
            return

        # ---- wait for login ----
        self.sig_status.emit("Waiting for login…")
        self.sig_log.emit("Please log in (scan QR code) in the embedded browser.")
        self._login_event.clear()
        self.sig_wait_login.emit()

        if not self._login_event.wait(timeout=600):  # 10 minutes
            self.sig_error.emit("Login timeout — could not detect course slides.")
            return
        if self._cancel_flag:
            self.sig_log.emit("Download cancelled.")
            return
        if self._login_count <= 0:
            self.sig_error.emit("No slides detected after login.")
            return

        total = self._login_count
        self.sig_status.emit(f"Found {total} slides")
        self.sig_progress.emit(0, total)

        # ---- capture each slide ----
        image_paths = []
        for i in range(total):
            if self._cancel_flag:
                self.sig_log.emit("Download cancelled.")
                break

            self._capture_event.clear()
            self.sig_capture.emit(i)

            if not self._capture_event.wait(timeout=60):
                self.sig_log.emit(f"Slide {i + 1}: capture timeout, skipping.")
                continue
            if self._cancel_flag:
                break

            if self._capture_ok:
                image_paths.append(self._capture_path)
            else:
                self.sig_log.emit(f"Slide {i + 1}: capture failed, skipping.")

            self.sig_progress.emit(i + 1, total)

        if not image_paths:
            self.sig_error.emit("No slides were captured.")
            return

        # ---- build PDF ----
        self.sig_status.emit("Building PDF…")
        self.sig_log.emit(f"Converting {len(image_paths)} images to PDF…")
        self._build_event.clear()
        self.sig_build_pdf.emit(image_paths, self._output_pdf)

        if not self._build_event.wait(timeout=60):
            self.sig_error.emit("PDF generation timeout.")
            return

        if self._build_result_path:
            self.sig_done.emit(self._build_result_path)
        else:
            self.sig_error.emit("PDF generation failed.")
