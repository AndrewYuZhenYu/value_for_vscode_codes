"""Entry point for ``python -m yuketang_downloader``."""

import sys


def main() -> None:
    from yuketang_downloader.gui.app import YuketangApp

    app = YuketangApp()
    app.mainloop()


if __name__ == "__main__":
    main()
