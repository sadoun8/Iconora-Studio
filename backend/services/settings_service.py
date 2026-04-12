import json
from pathlib import Path

from config import ICONORA_DOCS, PROJECTS_DIR


SETTINGS_FILE = ICONORA_DOCS / "settings.json"

DEFAULT_SETTINGS = {
    "theme": "dark",
    "language": "en",
    "default_quality": 95,
    "auto_open_folder": False,
    "ai_enabled": True,
    "ai_endpoint": "http://127.0.0.1:11434",
    "ai_model": "qwen2.5:7b-instruct",
    "ai_timeout": 30,
    "projects_dir": str(PROJECTS_DIR),
}


def load_settings() -> dict:
    if SETTINGS_FILE.exists():
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, dict):
                return {**DEFAULT_SETTINGS, **data}
        except Exception:
            pass
    return dict(DEFAULT_SETTINGS)


def save_settings(settings: dict) -> dict:
    ICONORA_DOCS.mkdir(parents=True, exist_ok=True)
    payload = {**DEFAULT_SETTINGS, **(settings or {})}
    with open(SETTINGS_FILE, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
    return payload
