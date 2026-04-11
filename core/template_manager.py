import json
from pathlib import Path

class TemplateManager:
    def __init__(self, template_folder="templates"):
        self.template_folder = Path(template_folder)

    def get_templates(self):
        templates = []
        if self.template_folder.exists():
            for file in self.template_folder.glob("*.json"):
                templates.append(file.stem)
        return templates

    def load_template(self, template_name):
        file_path = self.template_folder / f"{template_name}.json"
        if file_path.exists():
            with open(file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None
