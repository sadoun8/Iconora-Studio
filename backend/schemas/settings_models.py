from typing import Any

from pydantic import BaseModel


class SettingsDocument(BaseModel):
    theme: str = "dark"
    language: str = "en"
    default_quality: int = 95
    auto_open_folder: bool = False
    ai_enabled: bool = True
    ai_endpoint: str = "http://127.0.0.1:11434"
    ai_model: str = "qwen2.5:7b-instruct"
    ai_timeout: int = 30
    extra: dict[str, Any] = {}


class HealthResponse(BaseModel):
    status: str
    version: str
    desktop_mode: bool
    ai_enabled: bool


class BootstrapAssetsResponse(BaseModel):
    fonts: dict[str, list[dict[str, Any]]]
    templates: dict[str, list[dict[str, Any]]]
    icons: dict[str, list[dict[str, Any]]]
    ornaments: list[dict[str, Any]]
    sizes: dict[str, list[dict[str, Any]]]
    settings: dict[str, Any]
