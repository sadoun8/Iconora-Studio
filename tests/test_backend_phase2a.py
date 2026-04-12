from __future__ import annotations

import base64
import os
import shutil
import unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from uuid import uuid4

from fastapi import HTTPException
from PIL import Image

import backend.main as backend_main
import backend.api.routes_assets as routes_assets
import backend.api.routes_export as routes_export
import backend.api.routes_projects as routes_projects
import backend.api.routes_settings as routes_settings
import backend.services.assets_service as assets_service
import backend.services.export_service as export_service
import backend.services.settings_service as settings_service
import config
import core.project_manager as project_manager
from backend.schemas.export_models import ExportCanvasRequest
from backend.schemas.project_models import (
    ProjectExportRequest,
    SaveProjectRequest,
)


def _tiny_png_data_url(color=(255, 0, 0, 255)) -> str:
    image = Image.new("RGBA", (2, 2), color)
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


class Phase2ABackendVerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.run_root = Path.cwd() / ".test-scratch" / uuid4().hex
        self.run_root.mkdir(parents=True, exist_ok=False)
        self.addCleanup(lambda: shutil.rmtree(self.run_root, ignore_errors=True))

        self.docs_root = self.run_root / "Iconora Studio"
        self.exports_root = self.docs_root / "Exports"
        self.projects_root = self.docs_root / "Projects"
        self.logs_root = self.docs_root / "Logs"
        self.fonts_root = self.run_root / "assets" / "fonts"

        for directory in (
            self.docs_root,
            self.exports_root,
            self.projects_root,
            self.logs_root,
            self.fonts_root,
            self.exports_root / "Icons",
            self.exports_root / "SVGs",
            self.exports_root / "Logos",
            self.exports_root / "Signatures",
            self.exports_root / "Palettes",
        ):
            directory.mkdir(parents=True, exist_ok=True)

        # Minimal font assets keep bootstrap deterministic without depending on local machine fonts.
        (self.fonts_root / "Cairo.ttf").write_bytes(b"")
        (self.fonts_root / "Brand.otf").write_bytes(b"")

        self.temp_exports = {
            "Icons": self.exports_root / "Icons",
            "SVGs": self.exports_root / "SVGs",
            "Logos": self.exports_root / "Logos",
            "Signatures": self.exports_root / "Signatures",
            "Palettes": self.exports_root / "Palettes",
        }

        self.patchers = [
            patch.object(config, "ICONORA_DOCS", self.docs_root),
            patch.object(config, "EXPORTS_DIR", self.exports_root),
            patch.object(config, "PROJECTS_DIR", self.projects_root),
            patch.object(config, "LOG_DIR", self.logs_root),
            patch.object(config, "FONTS_DIR", self.fonts_root),
            patch.object(config, "EXPORT_SUBDIRS", self.temp_exports),
            patch.object(config, "APP_VERSION", "test-version"),
            patch.object(assets_service, "APP_VERSION", "test-version"),
            patch.object(assets_service, "APP_PHASE", "test-phase"),
            patch.object(settings_service, "ICONORA_DOCS", self.docs_root),
            patch.object(settings_service, "PROJECTS_DIR", self.projects_root),
            patch.object(settings_service, "SETTINGS_FILE", self.docs_root / "settings.json"),
            patch.object(assets_service, "FONTS_DIR", self.fonts_root),
            patch.object(export_service, "EXPORT_SUBDIRS", self.temp_exports),
            patch.object(
                export_service,
                "FORMAT_TO_DIR",
                {
                    "png": self.temp_exports["Logos"],
                    "webp": self.temp_exports["Logos"],
                    "pdf": self.temp_exports["Logos"],
                    "ico": self.temp_exports["Icons"],
                    "svg": self.temp_exports["SVGs"],
                },
            ),
            patch.object(project_manager, "PROJECTS_DIR", self.projects_root),
            patch.object(backend_main, "APP_VERSION", "test-version"),
            patch.dict(os.environ, {"ICONORA_DESKTOP_MODE": ""}, clear=False),
        ]

        for patcher in self.patchers:
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_health_endpoint_reflects_patched_settings(self) -> None:
        settings_service.save_settings({"ai_enabled": False, "language": "ar", "theme": "light"})

        payload = backend_main.health_check().model_dump()

        self.assertEqual(
            payload,
            {
                "status": "ok",
                "version": "test-version",
                "desktop_mode": False,
                "ai_enabled": False,
            },
        )

    def test_settings_get_reflects_boolean_flags_and_extra_keys(self) -> None:
        settings_service.save_settings(
            {
                "ai_enabled": False,
                "auto_open_folder": True,
                "language": "ar",
                "theme": "light",
                "custom_palette": "aurora",
            }
        )

        payload = routes_settings.get_settings().model_dump()

        self.assertFalse(payload["ai_enabled"])
        self.assertTrue(payload["auto_open_folder"])
        self.assertEqual(payload["language"], "ar")
        self.assertEqual(payload["theme"], "light")
        self.assertIn("custom_palette", payload["extra"])
        self.assertEqual(payload["extra"]["custom_palette"], "aurora")
        self.assertNotIn("ai_enabled", payload["extra"])
        self.assertNotIn("auto_open_folder", payload["extra"])

    def test_settings_put_persists_boolean_flags_and_extra_keys(self) -> None:
        request = routes_settings.SettingsDocument(
            theme="light",
            language="ar",
            auto_open_folder=True,
            ai_enabled=False,
            ai_endpoint="http://127.0.0.1:11434",
            ai_model="qwen2.5:7b-instruct",
            ai_timeout=42,
            extra={
                "custom_palette": "aurora",
                "show_tips": True,
            },
        )

        payload = routes_settings.update_settings(request).model_dump()

        self.assertEqual(payload["theme"], "light")
        self.assertEqual(payload["language"], "ar")
        self.assertTrue(payload["auto_open_folder"])
        self.assertFalse(payload["ai_enabled"])
        self.assertEqual(payload["ai_timeout"], 42)
        self.assertEqual(payload["extra"]["custom_palette"], "aurora")
        self.assertTrue(payload["extra"]["show_tips"])

        stored = settings_service.load_settings()
        self.assertFalse(stored["ai_enabled"])
        self.assertTrue(stored["auto_open_folder"])
        self.assertEqual(stored["custom_palette"], "aurora")
        self.assertTrue(stored["show_tips"])

    def test_bootstrap_assets_shape(self) -> None:
        payload = routes_assets.get_bootstrap().model_dump()

        self.assertEqual(set(payload), {"fonts", "templates", "icons", "ornaments", "sizes", "settings"})
        self.assertEqual(set(payload["fonts"]), {"general", "signature"})
        self.assertEqual(set(payload["templates"]), {"logo", "icon", "signature"})
        self.assertEqual(set(payload["icons"]), {"logo", "icon", "signature"})
        self.assertIsInstance(payload["ornaments"], list)
        self.assertEqual(set(payload["sizes"]), {"logo", "icon", "signature"})
        self.assertEqual(payload["settings"]["app_version"], "test-version")
        self.assertTrue(payload["settings"]["ai_enabled"])
        self.assertGreaterEqual(len(payload["templates"]["logo"]), 8)
        self.assertGreaterEqual(len(payload["icons"]["logo"]), 12)
        self.assertGreaterEqual(len(payload["ornaments"]), 8)

    def test_project_create_load_update_delete_flow(self) -> None:
        create_payload = {
            "name": "Phase 2A Project",
            "kind": "logo",
            "canvas": {"objects": [{"type": "text", "text": "Hello"}]},
            "assets": {"fonts": ["Cairo"]},
            "editor": {"section": "logo", "zoom": 1.25, "background": "#ffffff"},
            "export_defaults": {"format": "png", "width": 800, "height": 800},
        }

        created = routes_projects.create_project(SaveProjectRequest(**create_payload)).model_dump()
        self.assertEqual(created["name"], "Phase 2A Project")
        self.assertEqual(created["kind"], "logo")
        self.assertEqual(created["canvas"], create_payload["canvas"])
        self.assertEqual(created["editor"]["zoom"], 1.25)

        project_id = created["id"]

        listing = routes_projects.list_projects().model_dump()
        self.assertTrue(listing["success"])
        self.assertEqual(listing["count"], 1)
        self.assertEqual(listing["projects"][0]["id"], project_id)

        loaded = routes_projects.get_project(project_id).model_dump()
        self.assertEqual(loaded["id"], project_id)
        self.assertEqual(loaded["canvas"], create_payload["canvas"])

        updated_payload = {
            **create_payload,
            "canvas": {"objects": [{"type": "text", "text": "Updated"}]},
            "editor": {"section": "icon", "zoom": 0.75, "background": "#0f1115"},
        }
        updated = routes_projects.update_project(project_id, SaveProjectRequest(**updated_payload)).model_dump()
        self.assertEqual(updated["id"], project_id)
        self.assertEqual(updated["canvas"], updated_payload["canvas"])
        self.assertEqual(updated["editor"]["section"], "icon")

        delete_response = routes_projects.delete_project(project_id)
        self.assertTrue(delete_response["success"])

        with self.assertRaises(HTTPException) as exc_info:
            routes_projects.get_project(project_id)
        self.assertEqual(exc_info.exception.status_code, 404)

        final_list = routes_projects.list_projects().model_dump()
        self.assertEqual(final_list["count"], 0)

    def test_export_canvas_png_and_svg(self) -> None:
        png_payload = routes_export.export_canvas_route(
            ExportCanvasRequest(
                format="png",
                section="logo",
                width=2,
                height=2,
                transparent=False,
                data_url=_tiny_png_data_url(),
                filename="phase2a_png_smoke",
            )
        ).model_dump()
        self.assertTrue(png_payload["success"])
        self.assertTrue(png_payload["output_path"].endswith(".png"))
        self.assertTrue(Path(png_payload["output_path"]).exists())

        svg_payload = routes_export.export_canvas_route(
            ExportCanvasRequest(
                format="svg",
                section="logo",
                width=800,
                height=800,
                transparent=True,
                svg_text="<svg xmlns='http://www.w3.org/2000/svg' width='8' height='8'><rect width='8' height='8' fill='red'/></svg>",
                filename="phase2a_svg_smoke",
            )
        ).model_dump()
        self.assertTrue(svg_payload["success"])
        self.assertTrue(svg_payload["output_path"].endswith(".svg"))
        self.assertTrue(Path(svg_payload["output_path"]).exists())

    def test_project_export_payload_round_trip(self) -> None:
        created = routes_projects.create_project(
            SaveProjectRequest(
                name="Export Round Trip",
                kind="logo",
                canvas={"objects": []},
                assets={},
                editor={},
                export_defaults={},
            )
        )
        export_payload = routes_projects.export_project(
            ProjectExportRequest(project_id=created.id)
        )
        self.assertTrue(export_payload["success"])
        self.assertEqual(export_payload["document"]["id"], created.id)


if __name__ == "__main__":
    unittest.main()
