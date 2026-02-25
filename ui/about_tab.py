"""
About Tab
تبويب معلومات البرنامج

Professional About tab with license and version information
"""

import customtkinter as ctk
from core.license_manager import LicenseManager
import platform


class AboutTab(ctk.CTkFrame):
    """Professional About Tab with license and product information."""

    def __init__(self, master, license_manager: LicenseManager):
        super().__init__(master)
        self.license_manager = license_manager
        self._build_ui()

    def _build_ui(self):
        """Build about interface."""

        # Main scrollable container
        main = ctk.CTkScrollableFrame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Logo/Title section
        header_frame = ctk.CTkFrame(main, fg_color="#1a2a1a")
        header_frame.pack(fill="x", pady=(0, 20), padx=0)

        title = ctk.CTkLabel(
            header_frame,
            text="✨ Iconora Studio",
            font=("Arial", 28, "bold"),
            text_color="#d4af37"
        )
        title.pack(pady=(20, 5))

        version_edition = ctk.CTkLabel(
            header_frame,
            text=f"Version 1.0 - {self.license_manager.get_edition().title()} Edition",
            font=("Arial", 14),
            text_color="gray"
        )
        version_edition.pack(pady=(0, 20))

        # License info
        license_info = self.license_manager.get_license_info()

        info_frame = ctk.CTkFrame(main, fg_color="#1a1a1a")
        info_frame.pack(fill="x", pady=(0, 20))

        if license_info["licensed"]:
            status_text = f"🔒 Licensed to: {license_info['user']}"
            status_color = "#00CC66"
        else:
            status_text = "🔓 Demo Mode (Limited Features)"
            status_color = "#FFA500"

        status = ctk.CTkLabel(
            info_frame,
            text=status_text,
            font=("Arial", 12, "bold"),
            text_color=status_color
        )
        status.pack(pady=12)

        # Features
        features_label = ctk.CTkLabel(
            main,
            text="📦 Available Features:",
            font=("Arial", 13, "bold")
        )
        features_label.pack(anchor="w", pady=(15, 10))

        features_frame = ctk.CTkFrame(main, fg_color="#1a1a1a")
        features_frame.pack(fill="x", pady=(0, 20))

        features = license_info.get("features", [])

        feature_names = {
            "icon_convert": "💾 Icon Conversion (7 sizes)",
            "svg_convert": "🎨 SVG Conversion",
            "logo_designer": "🖼️ Logo Designer",
            "minimal_logo": "◼️ Minimal Logo Style",
            "all_logo_styles": "👑 All Logo Styles (Minimal, Luxury, 3D)",
            "signature_engine": "✍️ Professional Signature Engine",
            "palette_engine": "🎨 Smart Color Palette Generator",
            "project_manager": "📁 Project Management System",
            "batch_operations": "⚡ Batch Operations",
            "api_access": "🔌 REST API Access",
            "priority_support": "🎯 Priority Support",
            "custom_fonts": "🔤 Custom Font Support"
        }

        for feature in features:
            if feature == "all":
                continue  # Skip "all" marker

            feature_text = feature_names.get(feature, feature)
            feature_label = ctk.CTkLabel(
                features_frame,
                text=f"✅ {feature_text}",
                font=("Arial", 11),
                text_color="#00CC66",
                justify="left"
            )
            feature_label.pack(anchor="w", padx=15, pady=4)

        # Unavailable features in demo
        if not license_info["licensed"]:
            unavailable = ["svg_convert", "logo_designer", "all_logo_styles",
                         "signature_engine", "palette_engine", "project_manager",
                         "batch_operations", "api_access", "priority_support"]

            unavail_label = ctk.CTkLabel(
                main,
                text="🔒 Pro Features (Locked in Demo):",
                font=("Arial", 13, "bold"),
                text_color="#FF6B6B"
            )
            unavail_label.pack(anchor="w", pady=(15, 10))

            unavail_frame = ctk.CTkFrame(main, fg_color="#1a1a1a")
            unavail_frame.pack(fill="x", pady=(0, 20))

            for feature in unavailable:
                feature_text = feature_names.get(feature, feature)
                feature_label = ctk.CTkLabel(
                    unavail_frame,
                    text=f"🔒 {feature_text}",
                    font=("Arial", 11),
                    text_color="#FF8888",
                    justify="left"
                )
                feature_label.pack(anchor="w", padx=15, pady=4)

        # Developer info
        dev_label = ctk.CTkLabel(
            main,
            text="👨‍💻 Developer",
            font=("Arial", 13, "bold")
        )
        dev_label.pack(anchor="w", pady=(15, 10))

        dev_info = ctk.CTkLabel(
            main,
            text="Sadoun Al-Ardawi\nIconora Studio Project\n© 2026 All Rights Reserved",
            font=("Arial", 11),
            text_color="gray",
            justify="left"
        )
        dev_info.pack(anchor="w", pady=(0, 20))

        # Technical info
        tech_label = ctk.CTkLabel(
            main,
            text="⚙️ System Information",
            font=("Arial", 13, "bold")
        )
        tech_label.pack(anchor="w", pady=(15, 10))

        python_version = platform.python_version()
        system = platform.system()

        tech_info = ctk.CTkLabel(
            main,
            text=f"Python: {python_version}\nOS: {system}\nApp Version: 1.0\nBuild: Phase 6 Commercial",
            font=("Arial", 10),
            text_color="gray",
            justify="left"
        )
        tech_info.pack(anchor="w", pady=(0, 20))

        # Links
        links_label = ctk.CTkLabel(
            main,
            text="🌐 Resources",
            font=("Arial", 13, "bold")
        )
        links_label.pack(anchor="w", pady=(15, 10))

        links_frame = ctk.CTkFrame(main)
        links_frame.pack(fill="x", pady=(0, 20))

        links = [
            ("📖 Documentation", "https://github.com/sadoun/iconora-studio"),
            ("💬 Support", "support@iconora.studio"),
            ("🐛 Report Bug", "bugs@iconora.studio"),
            ("💳 Buy License", "https://iconora.studio/buy")
        ]

        for name, url in links:
            link_btn = ctk.CTkButton(
                links_frame,
                text=name,
                command=lambda u=url: self._open_link(u),
                fg_color="#333333",
                height=30
            )
            link_btn.pack(fill="x", pady=5)

        # License activation button
        separator = ctk.CTkFrame(main, height=2, fg_color="#333333")
        separator.pack(fill="x", pady=20)

        if not license_info["licensed"]:
            activate_btn = ctk.CTkButton(
                main,
                text="🔓 Activate License",
                height=40,
                command=self._open_activation,
                fg_color="#d4af37",
                text_color="#000000",
                font=("Arial", 12, "bold")
            )
            activate_btn.pack(fill="x", pady=10)

    def _open_link(self, url):
        """Open link (placeholder for future implementation)."""
        import webbrowser
        try:
            webbrowser.open(url)
        except:
            pass

    def _open_activation(self):
        """Open activation window."""
        from ui.activation_window import ActivationWindow
        self.winfo_toplevel().after(100, lambda: ActivationWindow(self.winfo_toplevel(), self.license_manager))
