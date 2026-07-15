"""Background worker thread that runs the Playwright automation.

Communicates with the GUI thread via a queue.Queue carrying typed
message tuples: ("status", msg), ("progress", current, total),
("log", msg), ("error", msg), ("done", pdf_path).
"""

import os
import queue
import shutil
import threading
import time
from pathlib import Path


class DownloadWorker(threading.Thread):
    """Runs Playwright-based courseware screenshotting on a background thread.

    The worker uses Playwright's sync API to:
    1. Launch Chromium with a persistent login context.
    2. Navigate to the course URL and wait for the user to log in.
    3. Iterate through slide thumbnails, screenshot each slide.
    4. Convert all screenshots to a single PDF.
    5. Clean up temporary files.

    Communication with the GUI happens exclusively through the
    status_queue, carrying tuples of the form:
        ("status", str)           — high-level phase change
        ("progress", int, int)    — current_page, total_pages
        ("log", str)              — detailed message for the output area
        ("error", str)            — terminal error (worker will exit)
        ("done", str)             — success, carries the PDF path
    """

    # JavaScript snipped that removes the navigation overlay ("skin disease")
    # from the courseware page before each screenshot.
    _REMOVE_OVERLAY_JS = """
        const el = document.querySelector(
            '#app > div.viewContainer > div > section > main > div '
            + '> div.basePPTMain.basePPTInline > div > div.layout_body '
            + '> div.layout_right_switch'
        );
        if (el) { el.remove(); }
    """

    def __init__(
        self,
        course_url: str,
        save_dir: str,
        output_pdf: str,
        browser_cache_dir: str,
        status_queue: queue.Queue,
    ):
        super().__init__(daemon=True)
        self._course_url = course_url
        self._save_dir = save_dir
        self._output_pdf = output_pdf
        self._browser_cache_dir = browser_cache_dir
        self._queue = status_queue
        self._cancel_event = threading.Event()

    # ---- public API ----

    def cancel(self) -> None:
        """Request graceful cancellation.

        The worker will finish the current slide (if any) and then exit.
        """
        self._cancel_event.set()

    # ---- threading.Thread interface ----

    def run(self) -> None:
        try:
            self._do_download()
        except Exception as exc:
            self._emit("error", f"Unexpected error: {exc}")

    # ---- internal helpers ----

    def _emit(self, msg_type: str, *args) -> None:
        """Thread-safe: push a typed message to the GUI queue."""
        self._queue.put((msg_type, *args))

    def _is_cancelled(self) -> bool:
        return self._cancel_event.is_set()

    # ---- main download logic ----

    def _do_download(self) -> None:
        # 告诉 Playwright 去系统路径找浏览器，而不是在 .app 包内找
        import os as _os
        _browsers_path = _os.path.expanduser("~/Library/Caches/ms-playwright")
        if _os.path.isdir(_browsers_path):
            _os.environ["PLAYWRIGHT_BROWSERS_PATH"] = _browsers_path

        from playwright.sync_api import sync_playwright

        # ---- browser launch ----
        self._emit("status", "Launching browser…")
        self._emit("log", "Starting Chromium with persistent login context.")

        save_path = Path(self._save_dir)
        save_path.mkdir(parents=True, exist_ok=True)

        with sync_playwright() as p:
            context = p.chromium.launch_persistent_context(
                user_data_dir=self._browser_cache_dir,
                headless=False,
                viewport={"width": 1920, "height": 1080},
                args=["--force-device-scale-factor=1"],
            )

            if self._is_cancelled():
                context.close()
                return

            page = context.pages[0] if context.pages else context.new_page()

            # ---- navigate to course ----
            self._emit("status", "Loading course page…")
            self._emit("log", f"Navigating to: {self._course_url}")
            page.goto(self._course_url, timeout=0)

            # ---- wait for login / page render ----
            self._emit("status", "Waiting for login…")
            self._emit(
                "log",
                "If you are not logged in, please scan the QR code in the browser window.",
            )
            self._emit("log", "Waiting up to 2 minutes for the course page to appear…")

            try:
                page.wait_for_selector(".thumbImg-container", timeout=120_000)
            except Exception:
                self._emit(
                    "error",
                    "Could not detect course slides. Please check the URL or your login status.",
                )
                context.close()
                return

            # ---- count slides ----
            thumbnails = page.locator(".thumbImg-container")
            total_pages = thumbnails.count()

            if total_pages == 0:
                self._emit("error", "No slides found on this page.")
                context.close()
                return

            self._emit("status", f"Found {total_pages} slides")
            self._emit("progress", 0, total_pages)

            # ---- screenshot each slide ----
            image_paths: list[str] = []

            for i in range(total_pages):
                if self._is_cancelled():
                    self._emit("log", "Download cancelled by user.")
                    break

                try:
                    thumb = thumbnails.nth(i)
                    thumb.scroll_into_view_if_needed()
                    thumb.click()

                    # Wait for slide content (text, formulas) to render
                    time.sleep(2.0)

                    # Remove the navigation overlay right before screenshotting
                    page.evaluate(self._REMOVE_OVERLAY_JS)

                    img_path = save_path / f"page_{i + 1:03d}.png"
                    page.locator(".slide_layer").first.screenshot(path=str(img_path))
                    image_paths.append(str(img_path))

                    self._emit("progress", i + 1, total_pages)
                    self._emit("log", f"✓ Slide {i + 1}/{total_pages} captured")
                except Exception as exc:
                    self._emit("log", f"✗ Slide {i + 1} failed: {exc}")
                    continue

            context.close()

            # ---- build PDF ----
            if not image_paths:
                self._emit("error", "No slides were captured.")
                return

            self._emit("status", "Building PDF…")
            self._emit("log", f"Converting {len(image_paths)} images to PDF…")

            from yuketang_downloader.core.pdf_builder import build_pdf

            build_pdf(image_paths, self._output_pdf)

            # ---- clean up temp images ----
            try:
                shutil.rmtree(str(save_path))
                self._emit("log", "Temporary files cleaned up.")
            except OSError as exc:
                self._emit("log", f"Could not clean up temp directory: {exc}")

            self._emit("done", self._output_pdf)
