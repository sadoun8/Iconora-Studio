import os
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.api import routes_ai
from backend.api import routes_assets
from backend.api import routes_export
from backend.api import routes_projects
from backend.api import routes_settings
from backend.schemas.settings_models import HealthResponse
from backend.services.settings_service import load_settings
from config import APP_VERSION

app = FastAPI(title="Iconora Studio API")

# Allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes_ai.router, prefix="/api", tags=["ai"])
app.include_router(routes_assets.router, prefix="/api/assets", tags=["assets"])
app.include_router(routes_export.router, prefix="/api/export", tags=["export"])
app.include_router(routes_projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(routes_settings.router, prefix="/api/settings", tags=["settings"])

@app.get("/api/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    settings = load_settings()
    return HealthResponse(
        status="ok",
        version=APP_VERSION,
        desktop_mode=bool(os.environ.get("ICONORA_DESKTOP_MODE")),
        ai_enabled=bool(settings.get("ai_enabled", True)),
    )


STATIC_DIR = Path(__file__).parent / "static"
if STATIC_DIR.exists():
    app.mount("/", StaticFiles(directory=STATIC_DIR, html=True), name="frontend")
