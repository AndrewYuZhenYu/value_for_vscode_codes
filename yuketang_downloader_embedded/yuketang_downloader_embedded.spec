# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec for the Rain Classroom Downloader Embedded Edition.

Produces a macOS .app bundle with Qt WebEngine (Chromium) bundled inside.
No external Playwright or Chromium installation required.

Usage:
    pyinstaller yuketang_downloader_embedded.spec

Output:
    dist/Rain Classroom Downloader Embedded.app

Size: ~250-300 MB (QtWebEngine includes a full Chromium renderer).
"""

from pathlib import Path

_SPEC_DIR = Path(SPECPATH)  # pyright: ignore  # noqa: F821
_REPO_ROOT = _SPEC_DIR.parent  # repo root — both packages are importable from here

a = Analysis(
    [str(_SPEC_DIR / "__main__.py")],
    pathex=[str(_REPO_ROOT)],
    binaries=[],
    datas=[],
    hiddenimports=[
        # Qt WebEngine
        "PySide6.QtWebEngineWidgets",
        "PySide6.QtWebEngineCore",
        "PySide6.QtWebEngine",
        "PySide6.QtWebChannel",
        "PySide6.QtNetwork",
        # PDF libraries
        "img2pdf",
        "pikepdf",
        "lxml",
        "lxml.etree",
        "PIL",
        "PIL.Image",
        # Reused sibling package
        "yuketang_downloader",
        "yuketang_downloader.utils",
        "yuketang_downloader.utils.paths",
        "yuketang_downloader.utils.config",
        "yuketang_downloader.core",
        "yuketang_downloader.core.pdf_builder",
        # Qt platform plugins
        "PySide6.QtCore",
        "PySide6.QtGui",
        "PySide6.QtWidgets",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "unittest",
        "test",
        "email",
        "xmlrpc",
        "pydoc",
        "distutils",
        "tkinter",
        "_tkinter",
        "tkinter.test",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RainClassroomDownloaderEmbedded",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[
        # Qt frameworks are already compressed — UPX can corrupt them
        "Qt*",
        "PySide6*",
    ],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=True,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(_REPO_ROOT / "yuketang_downloader" / "Resources" / "icon.icns")],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=["Qt*", "PySide6*"],
    name="RainClassroomDownloaderEmbedded",
)

app = BUNDLE(
    coll,
    name="Rain Classroom Downloader Embedded.app",
    icon=str(_REPO_ROOT / "yuketang_downloader" / "Resources" / "icon.icns"),
    bundle_identifier="com.andrewyu.rainclassroom-downloader-embedded",
    info_plist={
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "12.0",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1.0.0",
        "CFBundleName": "Rain Classroom Downloader (Embedded)",
        "CFBundleDisplayName": "雨课堂下载器 (内嵌版)",
        "NSHumanReadableCopyright": "Copyright © 2026 Andrew Yu",
    },
)
