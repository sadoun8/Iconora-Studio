from fastapi import APIRouter, HTTPException

from backend.schemas.project_models import (
    ProjectDocument,
    ProjectExportRequest,
    ProjectImportRequest,
    ProjectListResponse,
    SaveProjectRequest,
)
from backend.services.project_service import ProjectService

router = APIRouter()


def get_service() -> ProjectService:
    return ProjectService()


@router.get("", response_model=ProjectListResponse)
def list_projects() -> ProjectListResponse:
    projects = get_service().list_projects()
    return ProjectListResponse(success=True, projects=projects, count=len(projects))


@router.post("", response_model=ProjectDocument)
def create_project(req: SaveProjectRequest) -> ProjectDocument:
    return get_service().save_project(req.model_dump())


@router.post("/import", response_model=ProjectDocument)
def import_project(req: ProjectImportRequest) -> ProjectDocument:
    return get_service().import_project(req.document, req.new_name)


@router.post("/export")
def export_project(req: ProjectExportRequest) -> dict:
    try:
        return {"success": True, "document": get_service().export_project(req.project_id)}
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.get("/{project_id}", response_model=ProjectDocument)
def get_project(project_id: str) -> ProjectDocument:
    project = get_service().load_project(project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.put("/{project_id}", response_model=ProjectDocument)
def update_project(project_id: str, req: SaveProjectRequest) -> ProjectDocument:
    return get_service().save_project(req.model_dump(), project_id=project_id)


@router.delete("/{project_id}")
def delete_project(project_id: str) -> dict:
    if not get_service().delete_project(project_id):
        raise HTTPException(status_code=404, detail="Project not found")
    return {"success": True, "message": f"Deleted project {project_id}"}
