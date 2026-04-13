from __future__ import annotations

import unittest
import sys
import os

# Ensure the backend module is discoverable for local runs
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import backend.main as backend_main
import backend.api.routes_assets as routes_assets
import backend.api.routes_settings as routes_settings

class RuntimeContractsVerificationTests(unittest.TestCase):
    def test_health_contract_structure(self) -> None:
        response = backend_main.health_check()
        data = response.model_dump()
        
        # Verify exact contract shape
        expected_keys = {"status", "version", "desktop_mode", "ai_enabled"}
        self.assertTrue(expected_keys.issubset(set(data.keys())), f"Missing keys in health contract. Got: {data.keys()}")
        
        self.assertIsInstance(data["status"], str)
        self.assertIsInstance(data["version"], str)
        self.assertIsInstance(data["desktop_mode"], bool)
        self.assertIsInstance(data["ai_enabled"], bool)

    def test_settings_contract_structure(self) -> None:
        response = routes_settings.get_settings()
        data = response.model_dump()
        
        # Verify exact contract shape
        expected_keys = {
            "theme", 
            "language", 
            "default_quality", 
            "auto_open_folder", 
            "ai_enabled", 
            "ai_endpoint", 
            "ai_model", 
            "ai_timeout", 
            "extra"
        }
        self.assertTrue(expected_keys.issubset(set(data.keys())), f"Missing keys in settings contract. Got: {data.keys()}")
        
        self.assertIsInstance(data["theme"], str)
        self.assertIsInstance(data["language"], str)
        self.assertIsInstance(data["default_quality"], int)
        self.assertIsInstance(data["auto_open_folder"], bool)
        self.assertIsInstance(data["ai_enabled"], bool)
        self.assertIsInstance(data["ai_endpoint"], str)
        self.assertIsInstance(data["ai_model"], str)
        self.assertIsInstance(data["ai_timeout"], int)
        self.assertIsInstance(data["extra"], dict)

    def test_bootstrap_assets_contract_structure(self) -> None:
        response = routes_assets.get_bootstrap()
        data = response.model_dump()
        
        # Verify exact contract shape
        expected_keys = {"fonts", "templates", "icons", "ornaments", "sizes", "settings"}
        self.assertTrue(expected_keys.issubset(set(data.keys())), f"Missing keys in bootstrap contract. Got: {data.keys()}")
        
        # Verify inner shapes
        self.assertIsInstance(data["fonts"], dict)
        self.assertIsInstance(data["templates"], dict)
        self.assertIsInstance(data["icons"], dict)
        self.assertIsInstance(data["sizes"], dict)
        self.assertIsInstance(data["ornaments"], list)
        self.assertIsInstance(data["settings"], dict)
        
        # Settings inner payload shape
        self.assertIn("app_version", data["settings"])
        self.assertIn("ai_enabled", data["settings"])

if __name__ == "__main__":
    unittest.main()
