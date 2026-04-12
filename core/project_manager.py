"""
Iconora Studio - Phase 5: Project Manager
Manages .iconora project files with save/load/export functionality
"""

import json
import os
from pathlib import Path
from datetime import datetime
import logging

from config import PROJECTS_DIR

logger = logging.getLogger(__name__)


class ProjectManager:
    """Manage Iconora project files"""

    PROJECT_EXTENSION = '.iconora'
    PROJECT_VERSION = '1.0'

    def __init__(self, projects_folder=None):
        """Initialize project manager"""
        self.projects_folder = str(projects_folder or PROJECTS_DIR)
        self.ensure_folder()

    def ensure_folder(self):
        """Ensure projects folder exists"""
        Path(self.projects_folder).mkdir(parents=True, exist_ok=True)

    def save_project(self, name, data):
        """Save project to .iconora file"""
        try:
            self.ensure_folder()

            # Sanitize project name
            safe_name = self._sanitize_filename(name)
            if not safe_name:
                raise ValueError("Project name is empty or invalid")
            project_path = Path(self.projects_folder) / (safe_name + self.PROJECT_EXTENSION)

            # Create project structure
            project_data = {
                'name': name,
                'version': self.PROJECT_VERSION,
                'created': datetime.now().isoformat(),
                'modified': datetime.now().isoformat(),
                'data': data
            }

            # Write to file
            with open(project_path, 'w', encoding='utf-8') as f:
                json.dump(project_data, f, indent=2, ensure_ascii=False)

            return {
                'success': True,
                'path': str(project_path),
                'message': f'Project "{name}" saved successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'path': None,
                'message': f'Failed to save project: {str(e)}'
            }

    def load_project(self, name):
        """Load project from .iconora file"""
        try:
            safe_name = self._sanitize_filename(name)
            project_path = Path(self.projects_folder) / (safe_name + self.PROJECT_EXTENSION)

            if not project_path.exists():
                raise FileNotFoundError(f"Project not found: {name}")

            with open(project_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)

            return {
                'success': True,
                'data': project_data,
                'message': f'Project "{name}" loaded successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Failed to load project: {str(e)}'
            }

    def list_projects(self):
        """List all available projects"""
        try:
            self.ensure_folder()
            projects = []

            for file_path in Path(self.projects_folder).glob(f'*{self.PROJECT_EXTENSION}'):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)

                    projects.append({
                        'name': data.get('name', file_path.stem),
                        'file': file_path.name,
                        'path': str(file_path),
                        'created': data.get('created', 'Unknown'),
                        'modified': data.get('modified', 'Unknown'),
                        'version': data.get('version', 'Unknown')
                    })
                except Exception:
                    logger.warning(f"Skipping invalid project file: {file_path}", exc_info=True)

            return {
                'success': True,
                'projects': projects,
                'count': len(projects)
            }
        except Exception as e:
            return {
                'success': False,
                'projects': [],
                'count': 0,
                'message': f'Failed to list projects: {str(e)}'
            }

    def delete_project(self, name):
        """Delete a project"""
        try:
            safe_name = self._sanitize_filename(name)
            project_path = Path(self.projects_folder) / (safe_name + self.PROJECT_EXTENSION)

            if not project_path.exists():
                raise FileNotFoundError(f"Project not found: {name}")

            project_path.unlink()

            return {
                'success': True,
                'message': f'Project "{name}" deleted successfully'
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Failed to delete project: {str(e)}'
            }

    def export_project(self, name, export_path):
        """Export project to external location"""
        try:
            # Load project
            load_result = self.load_project(name)
            if not load_result['success']:
                raise Exception(load_result['message'])

            # Ensure export folder exists
            Path(export_path).parent.mkdir(parents=True, exist_ok=True)

            # Write to export location
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(load_result['data'], f, indent=2, ensure_ascii=False)

            return {
                'success': True,
                'path': export_path,
                'message': f'Project "{name}" exported to {export_path}'
            }
        except Exception as e:
            return {
                'success': False,
                'path': None,
                'message': f'Failed to export project: {str(e)}'
            }

    def import_project(self, import_path, new_name=None):
        """Import project from external file"""
        try:
            if not os.path.exists(import_path):
                raise FileNotFoundError(f"Import file not found: {import_path}")

            with open(import_path, 'r', encoding='utf-8') as f:
                project_data = json.load(f)

            # Determine project name
            if new_name:
                name = new_name
            elif 'name' in project_data:
                name = project_data['name']
            else:
                name = Path(import_path).stem

            # Save as new project
            return self.save_project(name, project_data.get('data', project_data))
        except Exception as e:
            return {
                'success': False,
                'path': None,
                'message': f'Failed to import project: {str(e)}'
            }

    def create_template_project(self, template_type='icon_converter'):
        """Create a template project"""
        try:
            templates = {
                'icon_converter': {
                    'type': 'icon_converter',
                    'source_image': '',
                    'output_folder': 'exports/icons',
                    'sizes': [16, 32, 48, 64, 128, 256],
                    'format': 'ico'
                },
                'logo_designer': {
                    'type': 'logo_designer',
                    'text': 'My Logo',
                    'style': 'Minimal',
                    'color1': '#000000',
                    'color2': '#FFFFFF',
                    'font_size': 80,
                    'width': 500,
                    'height': 500
                },
                'signature': {
                    'type': 'signature',
                    'name': 'John Doe',
                    'title': 'Designer',
                    'color': '#000000',
                    'font_size': 60,
                    'width': 600,
                    'height': 200
                }
            }

            if template_type not in templates:
                raise ValueError(f"Unknown template type: {template_type}")

            template_data = templates[template_type]
            template_name = f"{template_type}_template"

            return self.save_project(template_name, template_data)
        except Exception as e:
            return {
                'success': False,
                'path': None,
                'message': f'Failed to create template: {str(e)}'
            }

    def _sanitize_filename(self, filename):
        """Sanitize filename for safe file creation"""
        import re
        # Remove invalid characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        # Replace spaces with underscores
        filename = filename.replace(' ', '_')
        # Limit length
        return filename[:100] if len(filename) > 100 else filename
