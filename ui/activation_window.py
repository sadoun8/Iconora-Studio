"""
Activation Window
نافذة التفعيل والترخيص

Professional activation dialog for Iconora Studio licensing
"""

import customtkinter as ctk
from core.license_manager import LicenseManager


class ActivationWindow(ctk.CTkToplevel):
    """Professional activation window for license management."""

    def __init__(self, parent, license_manager: LicenseManager):
        super().__init__(parent)

        self.license_manager = license_manager
        self.title("🔐 Iconora Studio - License Activation")
        self.geometry("500x450")
        self.resizable(False, False)

        # Center window
        self.transient(parent)
        self.grab_set()

        self.result = None
        self._build_ui()

    def _build_ui(self):
        """Build activation interface."""

        # Header
        header = ctk.CTkFrame(self, fg_color="#1a1a1a")
        header.pack(fill="x", padx=0, pady=0)

        title = ctk.CTkLabel(
            header,
            text="🔐 License Activation",
            font=("Arial", 18, "bold")
        )
        title.pack(pady=20, padx=20)

        subtitle = ctk.CTkLabel(
            header,
            text="Activate your copy of Iconora Studio Pro",
            font=("Arial", 11),
            text_color="gray"
        )
        subtitle.pack(padx=20)

        # Main content
        content = ctk.CTkFrame(self)
        content.pack(fill="both", expand=True, padx=25, pady=25)

        # User name
        ctk.CTkLabel(
            content,
            text="User Name:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.name_entry = ctk.CTkEntry(
            content,
            placeholder_text="Your name for license",
            font=("Arial", 11),
            height=35
        )
        self.name_entry.pack(fill="x", pady=(0, 15))

        # Edition selection
        ctk.CTkLabel(
            content,
            text="Edition:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        self.edition_menu = ctk.CTkOptionMenu(
            content,
            values=["Pro", "Enterprise"],
            font=("Arial", 11),
            height=35
        )
        self.edition_menu.set("Pro")
        self.edition_menu.pack(fill="x", pady=(0, 15))

        # License key
        ctk.CTkLabel(
            content,
            text="Activation Key:",
            font=("Arial", 12, "bold")
        ).pack(anchor="w", pady=(0, 5))

        key_frame = ctk.CTkFrame(content)
        key_frame.pack(fill="x", pady=(0, 15))

        self.key_entry = ctk.CTkEntry(
            key_frame,
            placeholder_text="Enter your activation key",
            font=("Courier", 10),
            height=35
        )
        self.key_entry.pack(side="left", fill="both", expand=True, padx=(0, 10))

        generate_btn = ctk.CTkButton(
            key_frame,
            text="Generate",
            width=100,
            height=35,
            command=self.generate_key
        )
        generate_btn.pack(side="right")

        # Info
        info_frame = ctk.CTkFrame(content, fg_color="#1a1a1a", corner_radius=8)
        info_frame.pack(fill="x", pady=(0, 20))

        info_text = ctk.CTkLabel(
            info_frame,
            text="💡 Click 'Generate' to create a key,\nthen 'Activate' to enable all Pro features.",
            font=("Arial", 10),
            text_color="gray",
            justify="left"
        )
        info_text.pack(padx=12, pady=12)

        # Buttons
        button_frame = ctk.CTkFrame(content)
        button_frame.pack(fill="x", pady=(0, 0))

        activate_btn = ctk.CTkButton(
            button_frame,
            text="✅ Activate License",
            height=40,
            font=("Arial", 12, "bold"),
            command=self.activate
        )
        activate_btn.pack(side="left", fill="both", expand=True, padx=(0, 10))

        cancel_btn = ctk.CTkButton(
            button_frame,
            text="Cancel",
            height=40,
            fg_color="#333333",
            font=("Arial", 12),
            command=self.cancel
        )
        cancel_btn.pack(side="left", fill="x")

        # Status
        self.status = ctk.CTkLabel(
            content,
            text="",
            font=("Arial", 10),
            text_color="gray"
        )
        self.status.pack(pady=(10, 0))

    def generate_key(self):
        """Generate activation key from user name."""
        name = self.name_entry.get().strip()
        edition = self.edition_menu.get().lower()

        if not name:
            self.status.configure(text="❌ Enter user name first", text_color="#FF4444")
            return

        key = self.license_manager.generate_key(name, edition)
        self.key_entry.delete(0, "end")
        self.key_entry.insert(0, key)
        self.status.configure(text="✅ Key generated", text_color="#00CC66")

    def activate(self):
        """Activate license."""
        name = self.name_entry.get().strip()
        key = self.key_entry.get().strip()
        edition = self.edition_menu.get().lower()

        if not name:
            self.status.configure(text="❌ Enter user name", text_color="#FF4444")
            return

        if not key:
            self.status.configure(text="❌ Enter activation key", text_color="#FF4444")
            return

        # Validate key
        if not self.license_manager.validate_key(name, key, edition):
            self.status.configure(text="❌ Invalid key", text_color="#FF4444")
            return

        # Save license
        result = self.license_manager.save_license(name, key, edition)

        if result["success"]:
            self.status.configure(text="✅ License activated!", text_color="#00CC66")
            self.result = True
            self.after(1500, self.destroy)
        else:
            self.status.configure(text=f"❌ {result['message']}", text_color="#FF4444")

    def cancel(self):
        """Cancel activation."""
        self.result = False
        self.destroy()
