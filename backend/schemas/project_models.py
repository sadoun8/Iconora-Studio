from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field


class ProjectSummary(BaseModel):
    id: str
    name: str
    kind: str
    version: str
    created_at: str
    updated_at: str


class ProjectDocument(BaseModel):
    id: str
    name: str
    kind: str = "logo"
    version: str = "1.0"
    created_at: str
    updated_at: str
    canvas: dict[str, Any]
    assets: dict[str, Any] = {}
    editor: dict[str, Any] = {}
    export_defaults: dict[str, Any] = {}


class SaveProjectRequest(BaseModel):
    id: str | None = None
    name: str
    kind: str = "logo"
    canvas: dict[str, Any]
    assets: dict[str, Any] = {}
    editor: dict[str, Any] = {}
    export_defaults: dict[str, Any] = {}


class ProjectListResponse(BaseModel):
    success: bool
    projects: list[ProjectSummary]
    count: int


class ProjectImportRequest(BaseModel):
    document: dict[str, Any]
    new_name: str | None = None


class ProjectExportRequest(BaseModel):
    project_id: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(tzinfo=None, microsecond=0).isoformat() + "Z"
