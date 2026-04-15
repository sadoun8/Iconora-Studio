from __future__ import annotations

import json
from pathlib import Path

from core.project_manager import ProjectManager

from backend.schemas.project_models import ProjectDocument, ProjectSummary, now_iso


class ProjectService:
    def __init__(self) -> None:
        self.manager = ProjectManager()

    def _project_path(self, project_id: str) -> Path:
        safe_id = self.manager._sanitize_filename(project_id)
        return Path(self.manager.projects_folder) / f"{safe_id}{self.manager.PROJECT_EXTENSION}"

    def _write_project_file(
        self,
        path: Path,
        *,
        name: str,
        version: str,
        created_at: str,
        updated_at: str,
        data: dict,
    ) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        raw = {
            "name": name,
            "version": version,
            "created": created_at,
            "modified": updated_at,
            "data": data,
        }
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(raw, handle, indent=2, ensure_ascii=False)

    def list_projects(self) -> list[ProjectSummary]:
        result = self.manager.list_projects()
        if not result.get("success"):
            return []
        projects: list[ProjectSummary] = []
        for item in result.get("projects", []):
            project_id = Path(item["file"]).stem
            data = self.load_project(project_id)
            kind = data.kind if data else "logo"
            projects.append(
                ProjectSummary(
                    id=project_id,
                    name=item["name"],
                    kind=kind,
                    version=item.get("version", "1.0"),
                    created_at=item.get("created", now_iso()),
                    updated_at=item.get("modified", now_iso()),
                )
            )
        return projects

    def load_project(self, project_id: str) -> ProjectDocument | None:
        path = self._project_path(project_id)
        if not path.exists():
            return None
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
        data = raw.get("data", {})
        return ProjectDocument(
            id=path.stem,
            name=raw.get("name", path.stem),
            kind=data.get("kind") or data.get("type") or "logo",
            version=raw.get("version", "1.0"),
            created_at=raw.get("created", now_iso()),
            updated_at=raw.get("modified", now_iso()),
            canvas=data.get("canvas", {}),
            assets=data.get("assets", {}),
            editor=data.get("editor", {}),
            export_defaults=data.get("export_defaults", {}),
        )

    def save_project(self, payload: dict, project_id: str | None = None) -> ProjectDocument:
        current = self.load_project(project_id) if project_id else None
        project_name = str(payload["name"]).strip()
        safe_project_name = self.manager._sanitize_filename(project_name)
        if not safe_project_name:
            raise ValueError("Project name is empty or invalid")

        created_at = current.created_at if current else now_iso()
        updated_at = now_iso()
        project_data = {
            "kind": payload.get("kind", current.kind if current else "logo"),
            "canvas": payload.get("canvas", current.canvas if current else {}),
            "assets": payload.get("assets", current.assets if current else {}),
            "editor": payload.get("editor", current.editor if current else {}),
            "export_defaults": payload.get("export_defaults", current.export_defaults if current else {}),
        }
        version = payload.get("version", current.version if current else self.manager.PROJECT_VERSION)
        target_path = self._project_path(project_name)
        current_path = self._project_path(project_id) if project_id else None

        # Prevent accidental overwrite when a rename targets another existing project.
        if (
            current_path is not None
            and target_path != current_path
            and target_path.exists()
        ):
            raise ValueError(f"Project name already exists: {project_name}")

        self._write_project_file(
            target_path,
            name=project_name,
            version=version,
            created_at=created_at,
            updated_at=updated_at,
            data=project_data,
        )

        if current_path and current_path != target_path and current_path.exists():
            current_path.unlink()

        path = target_path
        return self.load_project(path.stem)

    def delete_project(self, project_id: str) -> bool:
        result = self.manager.delete_project(project_id)
        return bool(result.get("success"))

    def import_project(self, document: dict, new_name: str | None = None) -> ProjectDocument:
        name = new_name or document.get("name") or "Imported Project"
        payload = {
            "name": name,
            "kind": document.get("kind", "logo"),
            "canvas": document.get("canvas", {}),
            "assets": document.get("assets", {}),
            "editor": document.get("editor", {}),
            "export_defaults": document.get("export_defaults", {}),
            "version": document.get("version", "1.0"),
        }
        return self.save_project(payload)

    def export_project(self, project_id: str) -> dict:
        document = self.load_project(project_id)
        if not document:
            raise FileNotFoundError(f"Project not found: {project_id}")
        return document.model_dump()
