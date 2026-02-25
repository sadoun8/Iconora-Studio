"""
Localization Module - نظام الترجمة والتعريب
Support for Arabic and English
يدعم العربية والإنجليزية
"""

# ============================================================
# 🌍 LOCALIZATION DICTIONARY - قاموس الترجمة
# ============================================================

TRANSLATIONS = {
    # ==================== MAIN WINDOW ====================
    "app_title": {
        "ar": "🎨 Iconora Studio",
        "en": "🎨 Iconora Studio"
    },
    "app_subtitle": {
        "ar": "أداة احترافية لتحويل الصور والتصميم",
        "en": "Professional Image Conversion & Design Tool"
    },

    # ==================== TABS ====================
    "tab_icon_converter": {
        "ar": "تحويل الأيقونات",
        "en": "Icon Converter"
    },
    "tab_svg_converter": {
        "ar": "تحويل SVG",
        "en": "SVG Converter"
    },
    "tab_logo_designer": {
        "ar": "تصميم الشعارات",
        "en": "Logo Designer"
    },
    "tab_signature_generator": {
        "ar": "مولد التوقيعات",
        "en": "Signature Generator"
    },

    # ==================== ICON TAB ====================
    "icon_tab_title": {
        "ar": "تحويل الصور إلى أيقونات",
        "en": "Convert Images to Icons"
    },
    "btn_select_image": {
        "ar": "📁 اختر صورة",
        "en": "📁 Select Image"
    },
    "no_image_selected": {
        "ar": "لم يتم اختيار صورة",
        "en": "No image selected"
    },
    "select_sizes": {
        "ar": "اختر الأحجام المطلوبة:",
        "en": "Select desired sizes:"
    },
    "preview": {
        "ar": "معاينة",
        "en": "Preview"
    },
    "btn_save_ico": {
        "ar": "💾 حفظ ICO",
        "en": "💾 Save ICO"
    },
    "btn_save_png": {
        "ar": "📸 حفظ PNG",
        "en": "📸 Export PNG"
    },

    # ==================== SIZE LABELS ====================
    "size_16": {
        "ar": "16x16 (رمز صغير)",
        "en": "16x16 (Favicon)"
    },
    "size_24": {
        "ar": "24x24 (صغيرة)",
        "en": "24x24 (Small)"
    },
    "size_32": {
        "ar": "32x32 (افتراضي)",
        "en": "32x32 (Default)"
    },
    "size_48": {
        "ar": "48x48 (متوسطة)",
        "en": "48x48 (Medium)"
    },
    "size_64": {
        "ar": "64x64 (كبيرة)",
        "en": "64x64 (Large)"
    },
    "size_128": {
        "ar": "128x128 (كبيرة جداً)",
        "en": "128x128 (Extra Large)"
    },
    "size_256": {
        "ar": "256x256 (فائقة)",
        "en": "256x256 (Ultra Large)"
    },

    # ==================== FILE DIALOGS ====================
    "dialog_select_image": {
        "ar": "اختر صورة",
        "en": "Select Image"
    },
    "dialog_image_type": {
        "ar": "صور",
        "en": "Images"
    },
    "dialog_all_files": {
        "ar": "جميع الملفات",
        "en": "All Files"
    },
    "dialog_save_ico": {
        "ar": "احفظ ملف الأيقونة",
        "en": "Save Icon File"
    },
    "dialog_ico_type": {
        "ar": "ملفات الأيقونة",
        "en": "Icon Files"
    },
    "dialog_select_folder": {
        "ar": "اختر مجلد الحفظ",
        "en": "Select Save Folder"
    },

    # ==================== MESSAGES - INFO ====================
    "msg_success": {
        "ar": "نجاح",
        "en": "Success"
    },
    "msg_saved_ico": {
        "ar": "تم الحفظ بنجاح: ",
        "en": "Saved successfully: "
    },
    "msg_saved_svg": {
        "ar": "تم الحفظ بنجاح: ",
        "en": "Saved successfully: "
    },
    "msg_saved_logo": {
        "ar": "تم إنشاء الشعار بنجاح: ",
        "en": "Logo created successfully: "
    },
    "msg_results": {
        "ar": "النتائج",
        "en": "Results"
    },
    "msg_image_info": {
        "ar": "الحجم: {width}x{height} | الصيغة: {format}",
        "en": "Size: {width}x{height} | Format: {format}"
    },
    "msg_saved_images": {
        "ar": "تم حفظ {count} صورة بنجاح\n\nالنتائج:\n",
        "en": "Successfully saved {count} images\n\nResults:\n"
    },
    "msg_saved_file": {
        "ar": "تم حفظ: {filename}",
        "en": "Saved: {filename}"
    },
    "msg_no_preview": {
        "ar": "لا توجد معاينة حالياً",
        "en": "No preview available"
    },
    "msg_file_saved_at": {
        "ar": "الملف محفوظ في:",
        "en": "File saved at:"
    },

    # ==================== MESSAGES - WARNING ====================
    "msg_warning": {
        "ar": "تحذير",
        "en": "Warning"
    },
    "msg_select_image_first": {
        "ar": "الرجاء اختيار صورة أولاً",
        "en": "Please select an image first"
    },
    "msg_select_size": {
        "ar": "اختر حجماً واحداً على الأقل",
        "en": "Select at least one size"
    },
    "msg_enter_logo_text": {
        "ar": "الرجاء إدخال اسم الشعار/الشركة",
        "en": "Please enter logo/company name"
    },
    "msg_generate_logo_first": {
        "ar": "الرجاء إنشاء الشعار أولاً",
        "en": "Please generate a logo first"
    },

    # ==================== MESSAGES - ERROR ====================
    "msg_error": {
        "ar": "خطأ",
        "en": "Error"
    },
    "msg_load_error": {
        "ar": "خطأ في تحميل الصورة:\n",
        "en": "Error loading image:\n"
    },
    "msg_save_error": {
        "ar": "خطأ في الحفظ: ",
        "en": "Error saving: "
    },
    "msg_file_error": {
        "ar": "خطأ في الملف: ",
        "en": "File error: "
    },
    "msg_error_in": {
        "ar": " خطأ في: {filename} - {error}",
        "en": " Error in: {filename} - {error}"
    },
    "msg_error_occurred": {
        "ar": "حدث خطأ:\n",
        "en": "An error occurred:\n"
    },
    "msg_python_error": {
        "ar": "خطأ في Python",
        "en": "Python Error"
    },
    "msg_missing_dependencies": {
        "ar": "المكتبات المطلوبة غير مثبتة",
        "en": "Required libraries not installed"
    },

    # ==================== STATUS MESSAGES ====================
    "status_loading": {
        "ar": "جاري التحميل...",
        "en": "Loading..."
    },
    "status_converting": {
        "ar": "جاري التحويل...",
        "en": "Converting..."
    },
    "status_saving": {
        "ar": "جاري الحفظ...",
        "en": "Saving..."
    },
    "status_complete": {
        "ar": "مكتمل ✅",
        "en": "Complete ✅"
    },

    # ==================== MENU & SETTINGS ====================
    "menu_file": {
        "ar": "ملف",
        "en": "File"
    },
    "menu_edit": {
        "ar": "تحرير",
        "en": "Edit"
    },
    "menu_view": {
        "ar": "عرض",
        "en": "View"
    },
    "menu_help": {
        "ar": "مساعدة",
        "en": "Help"
    },
    "menu_language": {
        "ar": "اللغة",
        "en": "Language"
    },
    "language_arabic": {
        "ar": "العربية",
        "en": "Arabic"
    },
    "language_english": {
        "ar": "الإنجليزية",
        "en": "English"
    },
    "menu_settings": {
        "ar": "الإعدادات",
        "en": "Settings"
    },
    "menu_about": {
        "ar": "عن البرنامج",
        "en": "About"
    },
    "menu_exit": {
        "ar": "خروج",
        "en": "Exit"
    },

    # ==================== HELP & DOCUMENTATION ====================
    "help_title": {
        "ar": "تعليمات الاستخدام",
        "en": "Help & Instructions"
    },
    "help_step1": {
        "ar": "1️⃣ اختر صورة من جهازك",
        "en": "1️⃣ Select an image from your computer"
    },
    "help_step2": {
        "ar": "2️⃣ اختر الأحجام المطلوبة",
        "en": "2️⃣ Select the desired sizes"
    },
    "help_step3": {
        "ar": "3️⃣ انقر على حفظ ICO أو حفظ PNG",
        "en": "3️⃣ Click Save ICO or Export PNG"
    },
    "help_step4": {
        "ar": "4️⃣ اختر مكان الحفظ وانتظر",
        "en": "4️⃣ Choose save location and wait"
    },
    "about_version": {
        "ar": "الإصدار: 1.2.0",
        "en": "Version: 1.2.0"
    },
    "about_description": {
        "ar": "تطبيق احترافي لتحويل الصور والتصميم",
        "en": "Professional image conversion and design tool"
    },

    # ==================== TOOLTIPS ====================
    "tooltip_select_image": {
        "ar": "اختر صورة من جهازك (PNG, JPG, BMP, إلخ)",
        "en": "Select an image from your computer (PNG, JPG, BMP, etc)"
    },
    "tooltip_sizes": {
        "ar": "حدد الأحجام التي تريد تصديرها",
        "en": "Select the sizes you want to export"
    },
    "tooltip_ico": {
        "ar": "حفظ جميع الأحجام في ملف ICO واحد",
        "en": "Save all sizes in a single ICO file"
    },
    "tooltip_png": {
        "ar": "حفظ كل حجم كصورة PNG منفصلة",
        "en": "Save each size as a separate PNG image"
    },

    # ==================== QUALITY SETTINGS ====================
    "quality_title": {
        "ar": "جودة التحويل",
        "en": "Conversion Quality"
    },
    "quality_high": {
        "ar": "عالية جداً",
        "en": "Very High"
    },
    "quality_normal": {
        "ar": "عادية",
        "en": "Normal"
    },
    "quality_fast": {
        "ar": "سريعة",
        "en": "Fast"
    },

    # ==================== SVG TAB ====================
    "btn_convert_svg": {
        "ar": "🔄 تحويل إلى SVG",
        "en": "🔄 Convert to SVG"
    },
    "lbl_image_preview": {
        "ar": "معاينة الصورة",
        "en": "Image Preview"
    },
    "lbl_image_files": {
        "ar": "صور",
        "en": "Images"
    },
    "lbl_all_files": {
        "ar": "جميع الملفات",
        "en": "All Files"
    },
    "dlg_select_image": {
        "ar": "اختر صورة",
        "en": "Select Image"
    },
    "lbl_error": {
        "ar": "خطأ",
        "en": "Error"
    },
    "lbl_filename": {
        "ar": "اسم الملف",
        "en": "Filename"
    },
    "lbl_dimensions": {
        "ar": "الأبعاد",
        "en": "Dimensions"
    },
    "lbl_size": {
        "ar": "الحجم",
        "en": "Size"
    },
    "lbl_ico_files": {
        "ar": "ملفات الأيقونة",
        "en": "Icon Files"
    },
    "dlg_save_ico": {
        "ar": "احفظ ملف الأيقونة",
        "en": "Save Icon File"
    },
    "msg_exported_files": {
        "ar": "تم تصدير الملفات",
        "en": "Files exported"
    },

    # ==================== LOGO TAB ====================
    "lbl_logo_settings": {
        "ar": "إعدادات الشعار",
        "en": "Logo Settings"
    },
    "lbl_logo_text": {
        "ar": "نص الشعار",
        "en": "Logo Text"
    },
    "placeholder_company_name": {
        "ar": "أدخل اسم الشركة/الشعار",
        "en": "Enter company/logo name"
    },
    "lbl_font": {
        "ar": "الخط",
        "en": "Font"
    },
    "lbl_font_size": {
        "ar": "حجم الخط",
        "en": "Font Size"
    },
    "lbl_text_color": {
        "ar": "لون النص",
        "en": "Text Color"
    },
    "lbl_bg_color": {
        "ar": "لون الخلفية",
        "en": "Background Color"
    },
    "lbl_effects": {
        "ar": "التأثيرات",
        "en": "Effects"
    },
    "opt_use_gradient": {
        "ar": "استخدام تدرج لوني",
        "en": "Use color gradient"
    },
    "opt_add_shadow": {
        "ar": "إضافة ظل",
        "en": "Add shadow"
    },
    "opt_blur_effect": {
        "ar": "تأثير ضبابي",
        "en": "Blur effect"
    },
    "lbl_preview": {
        "ar": "المعاينة",
        "en": "Preview"
    },
    "btn_generate_logo": {
        "ar": "إنشاء الشعار",
        "en": "Generate Logo"
    },
    "btn_save_logo": {
        "ar": "حفظ الشعار",
        "en": "Save Logo"
    },
    "lbl_png_files": {
        "ar": "صور PNG",
        "en": "PNG Images"
    },
}


class Localization:
    """نظام إدارة الترجمة والتعريب"""

    def __init__(self, language: str = "ar"):
        """
        Initialize localization

        Args:
            language: "ar" for Arabic, "en" for English
        """
        self.current_language = language if language in ["ar", "en"] else "ar"

    def get(self, key: str, **kwargs) -> str:
        """
        الحصول على نص مترجم
        Get translated text

        Args:
            key: مفتاح الترجمة / Translation key
            **kwargs: متغيرات للاستبدال / Variables for substitution

        Returns:
            النص المترجم / Translated text
        """
        if key not in TRANSLATIONS:
            return f"[{key}]"  # Return key if not found

        translation = TRANSLATIONS[key].get(self.current_language,
                                          TRANSLATIONS[key].get("en", f"[{key}]"))

        # استبدال المتغيرات / Replace variables
        if kwargs:
            try:
                translation = translation.format(**kwargs)
            except KeyError as e:
                print(f"Missing translation variable: {e}")

        return translation

    def set_language(self, language: str):
        """
        تغيير اللغة
        Change language

        Args:
            language: "ar" for Arabic, "en" for English
        """
        if language in ["ar", "en"]:
            self.current_language = language

    def get_language(self) -> str:
        """الحصول على اللغة الحالية / Get current language"""
        return self.current_language

    def is_arabic(self) -> bool:
        """التحقق من كون اللغة عربية / Check if language is Arabic"""
        return self.current_language == "ar"

    def is_english(self) -> bool:
        """التحقق من كون اللغة إنجليزية / Check if language is English"""
        return self.current_language == "en"


# إنشاء كائن ترجمة عام / Create global localization object
i18n = Localization("ar")  # الافتراضي: العربية / Default: Arabic


def tr(key: str, **kwargs) -> str:
    """
    دالة مختصرة للترجمة
    Shortcut function for translation

    Example:
        text = tr("app_title")
        message = tr("msg_image_info", width=100, height=100)
    """
    return i18n.get(key, **kwargs)


def set_language(language: str):
    """تعيين اللغة / Set language"""
    i18n.set_language(language)


def get_language() -> str:
    """الحصول على اللغة الحالية / Get current language"""
    return i18n.get_language()


# للاستخدام مباشرة / For direct usage
__all__ = ["i18n", "tr", "set_language", "get_language", "Localization", "TRANSLATIONS"]
