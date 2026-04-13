import unittest
from datetime import datetime, timezone

from backend.schemas.project_models import ProjectDocument
from backend.schemas.export_models import ExportResponse


class ExtendedContractsVerificationTests(unittest.TestCase):
    def test_project_document_contract_structure(self) -> None:
        """
        Verify the structure, mandatory keys, and types of ProjectDocument contract.
        """
        now_str = datetime.now(timezone.utc).isoformat()
        
        # Instantiate with minimal required fields
        doc = ProjectDocument(
            id="proj_123",
            name="My First Logo",
            created_at=now_str,
            updated_at=now_str,
            canvas={"objects": [], "background": "#fff"}
        )
        data = doc.model_dump()
        
        # Verify exact required keys
        expected_keys = {
            "id", "name", "kind", "version", 
            "created_at", "updated_at", "canvas", 
            "assets", "editor", "export_defaults"
        }
        self.assertTrue(expected_keys.issubset(set(data.keys())), f"Missing keys in ProjectDocument. Got: {data.keys()}")
        
        # Verify default values were assigned properly
        self.assertEqual(data["kind"], "logo")
        self.assertEqual(data["version"], "1.0")
        self.assertEqual(data["assets"], {})
        self.assertEqual(data["editor"], {})
        self.assertEqual(data["export_defaults"], {})
        
        # Verify types
        self.assertIsInstance(data["id"], str)
        self.assertIsInstance(data["name"], str)
        self.assertIsInstance(data["created_at"], str)
        self.assertIsInstance(data["canvas"], dict)
        self.assertIsInstance(data["assets"], dict)

    def test_export_response_contract_structure(self) -> None:
        """
        Verify the structure, mandatory keys, and types of ExportResponse contract.
        """
        # Instantiate with required fields
        resp = ExportResponse(
            success=True,
            message="Exported successfully",
            output_path="/path/to/exported.png"
        )
        data = resp.model_dump()
        
        # Verify exact required keys
        expected_keys = {"success", "message", "output_path", "warnings"}
        self.assertTrue(expected_keys.issubset(set(data.keys())), f"Missing keys in ExportResponse. Got: {data.keys()}")
        
        # Verify types & defaults
        self.assertIsInstance(data["success"], bool)
        self.assertIsInstance(data["message"], str)
        self.assertIsInstance(data["output_path"], str)
        self.assertIsInstance(data["warnings"], list)
        self.assertEqual(data["warnings"], [])
        
        # Verify optional output_path behavior
        resp_no_path = ExportResponse(success=False, message="Failed")
        data_no_path = resp_no_path.model_dump()
        self.assertIsNone(data_no_path["output_path"])


if __name__ == "__main__":
    unittest.main()
