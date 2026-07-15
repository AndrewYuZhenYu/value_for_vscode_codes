"""Main window content — form fields, progress bar, log output."""

import queue
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from yuketang_downloader.utils.paths import get_browser_cache_dir


class MainWindow(ttk.Frame):
    """The primary content frame containing all UI widgets.

    Layout (top → bottom):
      1. Form section — URL, save folder, PDF name
      2. Action buttons — Start / Cancel
      3. Progress bar + status label
      4. Scrollable log output area
    """

    def __init__(self, master, config, settings_path):
        super().__init__(master, padding=(20, 16))
        self._config = config
        self._settings_path = settings_path
        self._queue: queue.Queue = queue.Queue()
        self._worker = None

        self._build_ui()
        self._restore_state()
        self._poll_queue()

    # ================================================================
    #  UI construction
    # ================================================================

    def _build_ui(self) -> None:
        """Build all widgets in a single grid layout."""
        # ---- row 0: heading ----
        heading = ttk.Label(
            self,
            text="🚀 雨课堂课件下载器",
            font=("Helvetica", 16, "bold"),
        )
        heading.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))

        # ---- row 1: Course URL ----
        ttk.Label(self, text="课件网址 (URL):").grid(
            row=1, column=0, sticky="w", pady=4
        )
        self._url_var = tk.StringVar()
        self._url_entry = ttk.Entry(self, textvariable=self._url_var, width=60)
        self._url_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=8, pady=4)

        # ---- row 2: Save Directory ----
        ttk.Label(self, text="截图暂存目录:").grid(
            row=2, column=0, sticky="w", pady=4
        )
        self._dir_var = tk.StringVar()
        self._dir_entry = ttk.Entry(self, textvariable=self._dir_var)
        self._dir_entry.grid(row=2, column=1, sticky="ew", padx=(8, 4), pady=4)
        browse_btn = ttk.Button(self, text="浏览…", command=self._browse_dir)
        browse_btn.grid(row=2, column=2, sticky="w", pady=4)

        # ---- row 3: Output PDF Name ----
        ttk.Label(self, text="输出 PDF 文件名:").grid(
            row=3, column=0, sticky="w", pady=4
        )
        self._pdf_var = tk.StringVar()
        self._pdf_entry = ttk.Entry(self, textvariable=self._pdf_var)
        self._pdf_entry.grid(row=3, column=1, columnspan=2, sticky="ew", padx=8, pady=4)

        # ---- row 4: Action buttons ----
        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=4, column=0, columnspan=3, pady=(12, 8))

        self._start_btn = ttk.Button(
            btn_frame, text="▶ 开始下载", command=self._start
        )
        self._start_btn.pack(side="left", padx=(0, 8))

        self._cancel_btn = ttk.Button(
            btn_frame, text="⏹ 取消", command=self._cancel, state="disabled"
        )
        self._cancel_btn.pack(side="left")

        # ---- row 5: Progress bar ----
        self._progress_var = tk.IntVar(value=0)
        self._progress_bar = ttk.Progressbar(
            self,
            variable=self._progress_var,
            maximum=100,
            mode="determinate",
        )
        self._progress_bar.grid(
            row=5, column=0, columnspan=3, sticky="ew", pady=(4, 2)
        )

        # ---- row 6: Status label ----
        self._status_var = tk.StringVar(value="就绪 — 请输入课件网址后点击「开始下载」")
        self._status_label = ttk.Label(
            self, textvariable=self._status_var, foreground="#555"
        )
        self._status_label.grid(row=6, column=0, columnspan=3, sticky="w", pady=(0, 6))

        # ---- row 7: Log output ----
        log_frame = ttk.Frame(self)
        log_frame.grid(row=7, column=0, columnspan=3, sticky="nsew")

        self._log_text = tk.Text(
            log_frame,
            height=14,
            width=70,
            state="disabled",
            wrap="word",
            font=("Menlo", 10),
            background="#1e1e1e",
            foreground="#d4d4d4",
            insertbackground="#d4d4d4",
            relief="flat",
            borderwidth=0,
        )
        self._log_text.pack(side="left", fill="both", expand=True)

        log_scroll = ttk.Scrollbar(log_frame, command=self._log_text.yview)
        log_scroll.pack(side="right", fill="y")
        self._log_text.configure(yscrollcommand=log_scroll.set)

        # Configure grid weights — log area gets all extra space
        self.columnconfigure(1, weight=1)
        self.rowconfigure(7, weight=1)

    # ================================================================
    #  Actions
    # ================================================================

    def _browse_dir(self) -> None:
        """Open a native macOS folder picker."""
        path = filedialog.askdirectory(title="选择截图暂存目录")
        if path:
            self._dir_var.set(path)

    def _start(self) -> None:
        """Validate inputs and launch the download worker thread."""
        url = self._url_var.get().strip()
        if not url:
            messagebox.showerror("输入错误", "课件网址不能为空。")
            return

        save_dir = self._dir_var.get().strip()
        if not save_dir:
            save_dir = str(Path.home() / "Downloads" / "yuketang_temp")

        output_pdf = self._pdf_var.get().strip()
        if not output_pdf:
            output_pdf = "courseware.pdf"
        if not output_pdf.endswith(".pdf"):
            output_pdf += ".pdf"

        # Prevent double-start
        if self._worker and self._worker.is_alive():
            messagebox.showinfo("提示", "下载正在进行中，请等待完成或先取消。")
            return

        # Persist current settings
        self._config.last_save_dir = save_dir
        self._config.last_output_name = output_pdf
        self._config.save(self._settings_path)

        # Switch to "running" UI state
        self._set_ui_state(running=True)
        self._clear_log()

        # Launch worker
        from yuketang_downloader.core.downloader import DownloadWorker

        self._worker = DownloadWorker(
            course_url=url,
            save_dir=save_dir,
            output_pdf=output_pdf,
            browser_cache_dir=str(get_browser_cache_dir()),
            status_queue=self._queue,
        )
        self._worker.start()

    def _cancel(self) -> None:
        """Request graceful cancellation of the running download."""
        if self._worker and self._worker.is_alive():
            self._worker.cancel()
            self._append_log("⏸ 正在取消…（完成当前页后停止）")
            self._cancel_btn.configure(state="disabled")

    # ================================================================
    #  Queue polling (GUI ← Worker communication)
    # ================================================================

    def _poll_queue(self) -> None:
        """Drain the message queue every 100ms and update the UI."""
        try:
            while True:
                msg = self._queue.get_nowait()
                self._handle_message(msg)
        except queue.Empty:
            pass
        self.after(100, self._poll_queue)

    def _handle_message(self, msg: tuple) -> None:
        """Route a typed message from the worker to the correct UI update."""
        msg_type = msg[0]

        if msg_type == "status":
            self._status_var.set(msg[1])

        elif msg_type == "progress":
            current, total = msg[1], msg[2]
            if total > 0:
                self._progress_var.set(int(current / total * 100))
            self._status_var.set(f"📸 正在截取第 {current}/{total} 页…")

        elif msg_type == "log":
            self._append_log(msg[1])

        elif msg_type == "error":
            self._append_log(f"❌ 错误: {msg[1]}")
            messagebox.showerror("下载失败", msg[1])
            self._set_ui_state(running=False)

        elif msg_type == "done":
            self._progress_var.set(100)
            self._status_var.set("✅ 下载完成！")
            self._append_log(f"📦 PDF 已保存到: {msg[1]}")
            messagebox.showinfo(
                "下载完成",
                f"课件 PDF 已生成：\n\n{msg[1]}",
            )
            self._set_ui_state(running=False)

    # ================================================================
    #  UI helpers
    # ================================================================

    def _append_log(self, text: str) -> None:
        """Append a line to the log output area and auto-scroll to bottom."""
        self._log_text.configure(state="normal")
        self._log_text.insert("end", text + "\n")
        self._log_text.see("end")
        self._log_text.configure(state="disabled")

    def _clear_log(self) -> None:
        """Reset the log area and progress bar."""
        self._log_text.configure(state="normal")
        self._log_text.delete("1.0", "end")
        self._log_text.configure(state="disabled")
        self._progress_var.set(0)
        self._status_var.set("正在启动浏览器…")

    def _set_ui_state(self, running: bool) -> None:
        """Toggle between 'idle' and 'running' UI states.

        When running, all form fields and the Start button are disabled,
        and the Cancel button becomes active.
        """
        state = "disabled" if running else "normal"
        for widget in (self._url_entry, self._dir_entry, self._pdf_entry, self._start_btn):
            widget.configure(state=state)
        self._cancel_btn.configure(state="normal" if running else "disabled")

    def _restore_state(self) -> None:
        """Populate form fields from persisted configuration."""
        if self._config.last_save_dir:
            self._dir_var.set(self._config.last_save_dir)
        else:
            self._dir_var.set(str(Path.home() / "Downloads" / "yuketang_temp"))

        if self._config.last_output_name:
            self._pdf_var.set(self._config.last_output_name)
        else:
            self._pdf_var.set("courseware.pdf")
