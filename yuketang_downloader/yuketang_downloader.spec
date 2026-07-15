# -*- mode: python ; coding: utf-8 -*-
"""PyInstaller spec file for the Rain Classroom Downloader macOS .app bundle.

Usage:
    pyinstaller yuketang_downloader.spec

Output:
    dist/Rain Classroom Downloader.app
"""

import sys
from pathlib import Path

# ---- paths relative to this spec file ----
_SPEC_DIR = Path(SPECPATH)  # pyright: ignore  # noqa: F821

a = Analysis(
    [str(_SPEC_DIR / "__main__.py")],
    pathex=[str(_SPEC_DIR.parent)],  # repo root so "yuketang_downloader" is importable
    binaries=[],
    datas=[
        # We do NOT bundle Chromium (~341 MB).
        # The app checks at launch and guides the user to install it.
    ],
    hiddenimports=[
        "playwright.sync_api",
        "playwright._impl._api_structures",
        "playwright._impl._object_factory",
        "img2pdf",
        "pikepdf",
        "lxml",
        "lxml.etree",
        "PIL",
        "PIL.Image",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        "tkinter.test",
        "unittest",
        "test",
        "email",
        "xmlrpc",
        "pydoc",
        "distutils",
    ],
    noarchive=False,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="RainClassroomDownloader",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # macOS GUI app — no Terminal window
    disable_windowed_traceback=True,
    target_arch="arm64",
    codesign_identity=None,
    entitlements_file=None,
    icon=[str(_SPEC_DIR / "Resources" / "icon.icns")],
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="RainClassroomDownloader",
)

app = BUNDLE(
    coll,
    name="Rain Classroom Downloader.app",
    icon=str(_SPEC_DIR / "Resources" / "icon.icns"),
    bundle_identifier="com.andrewyu.rainclassroom-downloader",
    info_plist={
        "NSHighResolutionCapable": True,
        "LSMinimumSystemVersion": "12.0",
        "CFBundleShortVersionString": "1.0.0",
        "CFBundleVersion": "1.0.0",
        "CFBundleName": "Rain Classroom Downloader",
        "CFBundleDisplayName": "雨课堂下载器",
        "NSHumanReadableCopyright": "Copyright © 2026 Andrew Yu",
    },
)
