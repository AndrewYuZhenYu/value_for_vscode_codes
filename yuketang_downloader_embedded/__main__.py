"""Entry point for ``python -m yuketang_downloader_embedded``."""

import sys


def main() -> None:
    from yuketang_downloader_embedded.gui.app import EmbeddedYuketangApp

    app = EmbeddedYuketangApp(sys.argv)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
