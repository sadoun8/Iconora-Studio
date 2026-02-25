"""
Project Manager
مدير المشاريع

Professional project save/load system for .iconora format.
"""

import json
import os
from pathlib import Path
from datetime import datetime


class ProjectManager:
    """Manage Iconora Studio projects."""

    def __init__(self, projects_folder="projects"):
        self.projects_folder = projects_folder
        Path(projects_folder).mkdir(parents=True, exist_ok=True)

    def save_project(self, project_name, project_data):
        """Save project as .iconora format (JSON).

        Args:
            project_name: Name of project (without extension)
            project_data: Dict containing project information

        Returns:
            dict: {"success": bool, "path": str, "message": str}
        """
        try:
            # Ensure project data has metadata
            project_data["metadata"] = {
                "name": project_name,
                "created": project_data.get("metadata", {}).get("created", datetime.now().isoformat()),
                "modified": datetime.now().isoformat(),
                "version": "1.0"
            }

            # Create .iconora file
            file_path = os.path.join(self.projects_folder, f"{project_name}.iconora")

            # Avoid overwrite
            counter = 1
            base_path = file_path
            while os.path.exists(file_path):
                name, ext = os.path.splitext(base_path)
                file_path = f"{name}_{counter}{ext}"
                counter += 1

            # Write JSON
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=4, ensure_ascii=False)

            return {
                "success": True,
                "path": file_path,
                "message": f"Project saved: {os.path.basename(file_path)}"
            }

        except Exception as e:
            return {
                "success": False,
                "path": "",
                "message": f"Save failed: {e}"
            }

    def load_project(self, file_path):
        """Load project from .iconora file.

        Args:
            file_path: Path to .iconora file

        Returns:
            dict: Project data or error info
        """
        try:
            if not os.path.exists(file_path):
                return {
                    "success": False,
                    "data": None,
                    "message": "File not found"
                }

            with open(file_path, "r", encoding="utf-8") as f:
                project_data = json.load(f)

            return {
                "success": True,
                "data": project_data,
                "message": "Project loaded successfully"
            }

        except Exception as e:
            return {
                "success": False,
                "data": None,
                "message": f"Load failed: {e}"
            }

    def list_projects(self):
        """List all saved projects.

        Returns:
            list: Project file names
        """
        projects = []
        if os.path.exists(self.projects_folder):
            projects = [f for f in os.listdir(self.projects_folder) if f.endswith(".iconora")]
        return sorted(projects)

    def delete_project(self, file_path):
        """Delete a project file.

        Args:
            file_path: Path to .iconora file

        Returns:
            dict: {"success": bool, "message": str}
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return {
                    "success": True,
                    "message": "Project deleted"
                }
            else:
                return {
                    "success": False,
                    "message": "File not found"
                }

        except Exception as e:
            return {
                "success": False,
                "message": f"Delete failed: {e}"
            }

    def export_project(self, file_path, export_format="json"):
        """Export project to different format.

        Args:
            file_path: Path to .iconora file
            export_format: "json" or "txt"

        Returns:
            dict: Export result
        """
        try:
            result = self.load_project(file_path)
            if not result["success"]:
                return result

            project_data = result["data"]
            project_name = os.path.splitext(os.path.basename(file_path))[0]

            if export_format == "json":
                output_path = os.path.join(self.projects_folder, f"{project_name}_export.json")
                with open(output_path, "w", encoding="utf-8") as f:
                    json.dump(project_data, f, indent=4, ensure_ascii=False)

            elif export_format == "txt":
                output_path = os.path.join(self.projects_folder, f"{project_name}_export.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    for key, value in project_data.items():
                        f.write(f"{key}: {value}\n")

            return {
                "success": True,
                "path": output_path,
                "message": f"Exported to {export_format.upper()}"
            }

        except Exception as e:
            return {
                "success": False,
                "path": "",
                "message": f"Export failed: {e}"
            }

    def create_template_project(self, name, project_type="logo"):
        """Create a new project from template.

        Args:
            name: Project name
            project_type: "logo", "signature", "icon", "palette"

        Returns:
            dict: Create result
        """
        templates = {
            "logo": {
                "type": "logo",
                "text": "Untitled Logo",
                "font": "Arial",
                "size": 80,
                "style": "Minimal",
                "color": "#000000",
                "secondary_color": "#ffffff"
            },
            "signature": {
                "type": "signature",
                "name": "Your Name",
                "title": "Your Title",
                "font": "Arial",
                "ink_effect": True
            },
            "icon": {
                "type": "icon",
                "source": "",
                "sizes": [16, 32, 64, 128, 256]
            },
            "palette": {
                "type": "palette",
                "style": "Modern",
                "colors": []
            }
        }

        template = templates.get(project_type, templates["logo"])
        project_data = {"project_type": project_type, **template}

        return self.save_project(name, project_data)
