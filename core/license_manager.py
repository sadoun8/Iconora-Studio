"""
License Manager
مدير الترخيص و التفعيل

Professional license and activation system for Iconora Studio
"""

import hashlib
import os
import json
from datetime import datetime
from pathlib import Path


class LicenseManager:
    """Manage product licenses and activations."""

    def __init__(self, file="license.key"):
        self.file = file
        self.secret = "ICONORA_STUDIO_2026_ALPHA"
        self.app_version = "1.0"
        self.editions = {
            "demo": {"name": "Demo", "features": ["icon_convert", "minimal_logo"]},
            "pro": {
                "name": "Pro",
                "features": ["icon_convert", "svg_convert", "logo_designer",
                           "signature_engine", "palette_engine", "project_manager",
                           "all_logo_styles", "batch_operations"]
            },
            "enterprise": {
                "name": "Enterprise",
                "features": ["all"] + ["api_access", "priority_support", "custom_fonts"]
            }
        }

    def generate_key(self, user_name: str, edition: str = "pro") -> str:
        """Generate activation key for user.

        Args:
            user_name: User's name for license
            edition: License edition (demo, pro, enterprise)

        Returns:
            str: 16-character activation key
        """
        raw = f"{user_name}{edition}{self.secret}{self.app_version}"
        hash_result = hashlib.sha256(raw.encode()).hexdigest()
        return f"{hash_result[:8]}-{hash_result[8:12]}-{hash_result[12:16]}".upper()

    def validate_key(self, user_name: str, key: str, edition: str = "pro") -> bool:
        """Validate activation key.

        Args:
            user_name: User name
            key: Activation key to validate
            edition: License edition

        Returns:
            bool: True if key is valid
        """
        expected_key = self.generate_key(user_name, edition)
        return expected_key == key

    def save_license(self, user_name: str, key: str, edition: str = "pro") -> dict:
        """Save license to file.

        Args:
            user_name: User name
            key: Activation key
            edition: License edition

        Returns:
            dict: Result with success status
        """
        try:
            license_data = {
                "user_name": user_name,
                "key": key,
                "edition": edition,
                "activated": datetime.now().isoformat(),
                "version": self.app_version
            }

            with open(self.file, "w", encoding="utf-8") as f:
                json.dump(license_data, f, indent=2, ensure_ascii=False)

            return {"success": True, "message": f"License activated for {user_name}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}

    def load_license(self) -> dict:
        """Load license from file.

        Returns:
            dict: License data or None if not found
        """
        try:
            if not os.path.exists(self.file):
                return None

            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def is_licensed(self) -> bool:
        """Check if application is licensed.

        Returns:
            bool: True if valid license exists
        """
        license_data = self.load_license()
        if not license_data:
            return False

        # Validate stored license
        user = license_data.get("user_name")
        key = license_data.get("key")
        edition = license_data.get("edition", "demo")

        return self.validate_key(user, key, edition)

    def get_edition(self) -> str:
        """Get current license edition.

        Returns:
            str: Edition name (demo, pro, enterprise) or "demo" if unlicensed
        """
        license_data = self.load_license()
        if license_data and self.is_licensed():
            return license_data.get("edition", "demo")
        return "demo"

    def has_feature(self, feature: str) -> bool:
        """Check if feature is available in current license.

        Args:
            feature: Feature name to check

        Returns:
            bool: True if feature is available
        """
        edition = self.get_edition()
        features = self.editions.get(edition, {}).get("features", [])

        # Check if feature is in list or if "all" is in features
        return feature in features or "all" in features

    def get_available_features(self) -> list:
        """Get list of available features in current edition.

        Returns:
            list: List of available feature names
        """
        edition = self.get_edition()
        return self.editions.get(edition, {}).get("features", [])

    def get_edition_info(self, edition: str = None) -> dict:
        """Get information about edition.

        Args:
            edition: Edition name, or current edition if None

        Returns:
            dict: Edition information
        """
        if edition is None:
            edition = self.get_edition()

        return self.editions.get(edition, {})

    def delete_license(self) -> dict:
        """Delete stored license file.

        Returns:
            dict: Result with success status
        """
        try:
            if os.path.exists(self.file):
                os.remove(self.file)
            return {"success": True, "message": "License removed"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}

    def create_demo_license(self) -> None:
        """Create a demo license for testing."""
        self.save_license("Demo User", self.generate_key("Demo User", "demo"), "demo")

    def get_license_info(self) -> dict:
        """Get detailed license information.

        Returns:
            dict: License info or demo info if unlicensed
        """
        license_data = self.load_license()

        if license_data and self.is_licensed():
            return {
                "licensed": True,
                "user": license_data.get("user_name"),
                "edition": license_data.get("edition"),
                "activated": license_data.get("activated"),
                "features": self.get_available_features()
            }
        else:
            return {
                "licensed": False,
                "user": "Demo User",
                "edition": "demo",
                "features": ["icon_convert", "minimal_logo"],
                "message": "Limited Demo Mode"
            }
