"""Application settings persistence via JSON file."""

import json
from dataclasses import dataclass, field, asdict, fields
from pathlib import Path
from typing import Optional


@dataclass
class AppConfig:
    """User-configurable application settings.

    Persisted to ~/Library/Application Support/RainClassroomDownloader/settings.json
    """

    last_save_dir: str = ""
    last_output_name: str = "courseware.pdf"
    last_url: str = ""
    window_geometry: str = ""  # e.g. "800x600+100+100"
    browser_cache_dir: str = ""

    # ---- serialization ----

    @classmethod
    def load(cls, path: Path) -> "AppConfig":
        """Load config from disk, returning defaults if the file doesn't exist.

        On first run, writes the defaults back so the file always exists.
        """
        if path.exists():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                # Only pick known fields to ignore any stale keys
                known = {f.name for f in fields(cls)}
                filtered = {k: v for k, v in data.items() if k in known}
                return cls(**filtered)
            except (json.JSONDecodeError, TypeError):
                # Corrupt config — fall through to defaults
                pass

        config = cls()
        config.save(path)
        return config

    def save(self, path: Path) -> None:
        """Write current config to disk."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(asdict(self), indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    # ---- validation ----

    def validate(self) -> list[str]:
        """Return a list of warnings (non-fatal issues) about the current config.

        An empty list means everything looks fine.
        """
        warnings: list[str] = []
        if self.last_save_dir and not Path(self.last_save_dir).exists():
            warnings.append(f"Previous save directory no longer exists: {self.last_save_dir}")
        return warnings


