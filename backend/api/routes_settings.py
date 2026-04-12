from fastapi import APIRouter

from backend.schemas.settings_models import SettingsDocument
from backend.services.settings_service import load_settings, save_settings

router = APIRouter()


@router.get("", response_model=SettingsDocument)
def get_settings() -> SettingsDocument:
    settings = load_settings()
    extra = {k: v for k, v in settings.items() if k not in SettingsDocument.model_fields}
    return SettingsDocument(**{**settings, "extra": extra})


@router.put("", response_model=SettingsDocument)
def update_settings(req: SettingsDocument) -> SettingsDocument:
    payload = req.model_dump()
    extra = payload.pop("extra", {})
    merged = save_settings({**payload, **extra})
    return SettingsDocument(**{**merged, "extra": extra})
