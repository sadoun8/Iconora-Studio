"""
Main Window
النافذة الرئيسية للتطبيق

Main Application Window with full Arabic support and license management
"""

import customtkinter as ctk
from ui.icon_tab import IconTab
from ui.svg_tab import SVGTab
from ui.logo_tab import LogoTab
from ui.signature_tab import SignatureTab
from ui.about_tab import AboutTab
from ui.activation_window import ActivationWindow
from core.license_manager import LicenseManager
from i18n import tr, get_language, set_language


class MainWindow(ctk.CTk):
    """النافذة الرئيسية للتطبيق / Main Application Window with License System"""

    def __init__(self):
        super().__init__()

        # Initialize license manager
        self.license_manager = LicenseManager()

        # إعدادات النافذة / Window settings
        edition = self.license_manager.get_edition()
        edition_label = f"({edition.title()})"
        self.title(f"Iconora Studio {edition_label} - أداة تحويل الأيقونات والتصميم المحترفة")
        self.geometry("1200x750")
        self.minsize(900, 600)

        # تعيين المظهر / Set theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # إعداد الواجهة / Setup UI
        self.setup_ui()

        # Check if demo and show activation prompt after delay
        if not self.license_manager.is_licensed():
            self.after(2000, self._show_demo_notification)

    def setup_ui(self):
        """إعداد واجهة المستخدم / Setup user interface"""

        # شريط علوي / Header bar
        header = ctk.CTkFrame(self, fg_color="#1a1a1a")
        header.pack(fill="x", padx=0, pady=0)

        # شعار التطبيق / App logo
        title = ctk.CTkLabel(
            header,
            text=tr("app_title"),
            font=("Arial", 24, "bold")
        )
        title.pack(side="left", padx=20, pady=15)

        subtitle = ctk.CTkLabel(
            header,
            text=tr("app_subtitle"),
            font=("Arial", 11),
            text_color="gray"
        )
        subtitle.pack(side="left", padx=5)

        # License status indicator
        license_info = self.license_manager.get_license_info()
        if license_info["licensed"]:
            license_text = f"🔒 {license_info['user']}"
            license_color = "#00CC66"
        else:
            license_text = "🔓 Demo Mode"
            license_color = "#FFA500"

        license_label = ctk.CTkLabel(
            header,
            text=license_text,
            font=("Arial", 10),
            text_color=license_color
        )
        license_label.pack(side="left", padx=20)

        # أزرار اللغة والتفعيل / Language and activation buttons
        controls_frame = ctk.CTkFrame(header, fg_color="#1a1a1a")
        controls_frame.pack(side="right", padx=20)

        # Activate button if demo
        if not license_info["licensed"]:
            activate_btn = ctk.CTkButton(
                controls_frame,
                text="🔓 Activate",
                command=self._open_activation,
                width=110,
                height=30,
                fg_color="#d4af37",
                text_color="#000000"
            )
            activate_btn.pack(side="left", padx=5)

        ar_btn = ctk.CTkButton(
            controls_frame,
            text="العربية 🇸🇦",
            command=lambda: self.change_language("ar"),
            width=100,
            height=30
        )
        ar_btn.pack(side="left", padx=5)

        en_btn = ctk.CTkButton(
            controls_frame,
            text="English 🇬🇧",
            command=lambda: self.change_language("en"),
            width=100,
            height=30
        )
        en_btn.pack(side="left", padx=5)

        # نطاق التبويبات / Tab view
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(fill="both", expand=True, padx=10, pady=10)

        # تبويب تحويل الأيقونات (المرحلة 1) / Icon converter tab
        self.icon_tab = self.tab_view.add("💾 " + tr("tab_icon_converter"))
        self.icon_content = IconTab(self.icon_tab)
        self.icon_content.pack(fill="both", expand=True)

        # تبويب تحويل SVG (المرحلة 2) / SVG converter tab - Check license
        if self.license_manager.has_feature("svg_convert"):
            self.svg_tab = self.tab_view.add("🎨 " + tr("tab_svg_converter"))
            self.svg_content = SVGTab(self.svg_tab)
            self.svg_content.pack(fill="both", expand=True)
        else:
            locked_tab = self.tab_view.add("🔒 " + tr("tab_svg_converter"))
            self._create_locked_tab(locked_tab, "SVG Converter")

        # تبويب تصميم الشعارات (المرحلة 3-4) / Logo designer tab - Check license
        if self.license_manager.has_feature("logo_designer"):
            self.logo_tab = self.tab_view.add("🖼️ " + tr("tab_logo_designer"))
            self.logo_content = LogoTab(self.logo_tab)
            self.logo_content.pack(fill="both", expand=True)
        else:
            locked_tab = self.tab_view.add("🔒 " + tr("tab_logo_designer"))
            self._create_locked_tab(locked_tab, "Logo Designer")

        # تبويب التوقيع (المرحلة 5) / Signature generator tab - Check license
        if self.license_manager.has_feature("signature_engine"):
            self.signature_tab = self.tab_view.add("✍️ " + tr("tab_signature_generator"))
            self.signature_content = SignatureTab(self.signature_tab)
            self.signature_content.pack(fill="both", expand=True)
        else:
            locked_tab = self.tab_view.add("🔒 " + tr("tab_signature_generator"))
            self._create_locked_tab(locked_tab, "Signature Engine")

        # تبويب About (المرحلة 6) / About tab
        self.about_tab = self.tab_view.add("ℹ️ About")
        self.about_content = AboutTab(self.about_tab, self.license_manager)
        self.about_content.pack(fill="both", expand=True)

    def _create_locked_tab(self, parent, feature_name):
        """Create a locked feature tab."""
        frame = ctk.CTkFrame(parent)
        frame.pack(fill="both", expand=True)

        center_frame = ctk.CTkFrame(frame)
        center_frame.place(relx=0.5, rely=0.5, anchor="center")

        lock_label = ctk.CTkLabel(
            center_frame,
            text="🔒",
            font=("Arial", 80),
            text_color="#FF8888"
        )
        lock_label.pack(pady=20)

        title = ctk.CTkLabel(
            center_frame,
            text=f"{feature_name} - Pro Feature",
            font=("Arial", 18, "bold"),
            text_color="#FF8888"
        )
        title.pack(pady=10)

        text = ctk.CTkLabel(
            center_frame,
            text="This feature is only available in Pro Edition.\nClick 'Activate' to unlock all features.",
            font=("Arial", 12),
            text_color="gray"
        )
        text.pack(pady=20)

        activate_btn = ctk.CTkButton(
            center_frame,
            text="🔓 Activate License",
            command=self._open_activation,
            height=40,
            font=("Arial", 12, "bold"),
            fg_color="#d4af37",
            text_color="#000000"
        )
        activate_btn.pack(pady=20)

    def _open_activation(self):
        """Open activation window."""
        ActivationWindow(self, self.license_manager)
        # Reload UI after potential license change
        self.after(2000, self._reload_after_activation)

    def _reload_after_activation(self):
        """Reload application after license activation."""
        if self.license_manager.is_licensed():
            self.destroy()
            app = MainWindow()
            app.run()

    def _show_demo_notification(self):
        """Show demo mode notification."""
        from tkinter import messagebox
        messagebox.showinfo(
            "Demo Mode",
            "Welcome to Iconora Studio!\n\n"
            "You're using the Demo Mode with limited features.\n\n"
            "Click the 'Activate' button to unlock all Pro features."
        )


    def change_language(self, language: str):
        """تغيير اللغة / Change language"""
        set_language(language)
        # إعادة تحميل الواجهة / Reload UI
        self.destroy()
        app = MainWindow()
        app.run()

    def run(self):
        """تشغيل التطبيق"""
        self.mainloop()


if __name__ == "__main__":
    app = MainWindow()
    app.run()
