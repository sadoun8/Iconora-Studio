"""
Feature Restrictions
قيود الميزات حسب الترخيص

Helper utilities for enforcing license-based feature restrictions
"""

from core.license_manager import LicenseManager


class FeatureGuard:
    """Guard access to features based on license."""

    def __init__(self):
        self.license_manager = LicenseManager()

    def check_feature(self, feature: str) -> bool:
        """Check if feature is available.

        Args:
            feature: Feature name

        Returns:
            bool: True if feature is available
        """
        return self.license_manager.has_feature(feature)

    def require_feature(self, feature: str, feature_name: str) -> bool:
        """Require a feature and show dialog if unavailable.

        Args:
            feature: Feature key
            feature_name: Display name

        Returns:
            bool: True if available, False otherwise
        """
        if not self.check_feature(feature):
            import tkinter.messagebox as mb
            response = mb.showwarning(
                "Pro Feature Required",
                f"{feature_name} is only available in Pro Edition.\n\n"
                "Would you like to activate your license?"
            )
            return False
        return True

    def get_restrictions_message(self) -> str:
        """Get message about current restrictions.

        Returns:
            str: Human-readable message
        """
        edition = self.license_manager.get_edition()

        if edition == "pro" or edition == "enterprise":
            return "✅ All features unlocked!"
        else:
            return "🔒 Demo Mode: Limited to Icon Conversion and Minimal Logos"

    def is_pro(self) -> bool:
        """Check if Pro or Enterprise edition.

        Returns:
            bool: True if Pro or higher
        """
        edition = self.license_manager.get_edition()
        return edition in ["pro", "enterprise"]

    def is_enterprise(self) -> bool:
        """Check if Enterprise edition.

        Returns:
            bool: True if Enterprise
        """
        return self.license_manager.get_edition() == "enterprise"


# Global instance
feature_guard = FeatureGuard()
