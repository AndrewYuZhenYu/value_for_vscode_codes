"""macOS-standard filesystem paths for the application."""

from pathlib import Path


def get_app_support_dir() -> Path:
    """Return ~/Library/Application Support/RainClassroomDownloader/

    This is the macOS-standard location for per-user application data.
    The directory is NOT created here — callers should mkdir as needed.
    """
    return Path.home() / "Library" / "Application Support" / "RainClassroomDownloader"


def get_browser_cache_dir() -> Path:
    """Return the persistent Chromium user data directory.

    Stores login cookies and session state so the user doesn't need
    to scan the QR code on every launch.
    """
    return get_app_support_dir() / "browser_cache"


def get_settings_path() -> Path:
    """Return the path to settings.json."""
    return get_app_support_dir() / "settings.json"


def get_default_downloads_dir() -> Path:
    """Return ~/Downloads as the fallback save directory."""
    return Path.home() / "Downloads"
