from fastapi import APIRouter

from backend.schemas.settings_models import BootstrapAssetsResponse
from backend.services.assets_service import get_bootstrap_assets

router = APIRouter()


@router.get("/bootstrap", response_model=BootstrapAssetsResponse)
def get_bootstrap() -> BootstrapAssetsResponse:
    return BootstrapAssetsResponse(**get_bootstrap_assets())
