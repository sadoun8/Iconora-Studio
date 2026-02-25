"""
Language and Localization Configuration
إعدادات اللغة والتعريب
"""

import os
import json
from pathlib import Path

# ============================================================
# 🌍 LANGUAGE CONFIGURATION
# ============================================================

# المجلد الافتراضي للإعدادات / Default settings directory
CONFIG_DIR = Path.home() / ".iconora"
CONFIG_FILE = CONFIG_DIR / "settings.json"

# اللغة الافتراضية / Default language
DEFAULT_LANGUAGE = "ar"  # عربي / Arabic

# اللغات المدعومة / Supported languages
SUPPORTED_LANGUAGES = {
    "ar": {
        "name": "العربية",
        "name_en": "Arabic",
        "flag": "🇸🇦",
        "direction": "rtl"  # Right-to-left
    },
    "en": {
        "name": "English",
        "name_ar": "الإنجليزية",
        "flag": "🇬🇧",
        "direction": "ltr"  # Left-to-right
    }
}


class LanguageManager:
    """نظام إدارة اللغة والإعدادات / Language and settings management system"""

    def __init__(self):
        """تهيئة مدير اللغة / Initialize language manager"""
        self.config_dir = CONFIG_DIR
        self.config_file = CONFIG_FILE
        self.settings = self.load_settings()
        self.current_language = self.settings.get("language", DEFAULT_LANGUAGE)

    def load_settings(self) -> dict:
        """تحميل الإعدادات المحفوظة / Load saved settings"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")

        return {"language": DEFAULT_LANGUAGE}

    def save_settings(self):
        """حفظ الإعدادات / Save settings"""
        try:
            self.config_dir.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def set_language(self, language: str):
        """تعيين اللغة / Set language"""
        if language in SUPPORTED_LANGUAGES:
            self.current_language = language
            self.settings["language"] = language
            self.save_settings()
            return True
        return False

    def get_language(self) -> str:
        """الحصول على اللغة الحالية / Get current language"""
        return self.current_language

    def get_language_name(self, lang_code: str = None) -> str:
        """الحصول على اسم اللغة / Get language name"""
        if lang_code is None:
            lang_code = self.current_language

        lang_info = SUPPORTED_LANGUAGES.get(lang_code, {})

        if self.current_language == "ar":
            return lang_info.get("name", "غير معروف")
        else:
            return lang_info.get("name_en", lang_info.get("name", "Unknown"))

    def get_direction(self) -> str:
        """الحصول على اتجاه النص / Get text direction (rtl for Arabic, ltr for English)"""
        lang_info = SUPPORTED_LANGUAGES.get(self.current_language, {})
        return lang_info.get("direction", "ltr")

    def is_arabic(self) -> bool:
        """التحقق من كون اللغة عربية / Check if current language is Arabic"""
        return self.current_language == "ar"

    def is_english(self) -> bool:
        """التحقق من كون اللغة إنجليزية / Check if current language is English"""
        return self.current_language == "en"


# إنشاء مثيل عام / Create global instance
language_manager = LanguageManager()


# دوال عام تيسيرة / Convenient functions
def get_current_language() -> str:
    """الحصول على اللغة الحالية / Get current language"""
    return language_manager.get_language()


def set_current_language(language: str):
    """تعيين اللغة / Set current language"""
    language_manager.set_language(language)


def get_text_direction() -> str:
    """الحصول على اتجاه النص / Get text direction"""
    return language_manager.get_direction()


def is_rtl() -> bool:
    """التحقق من أن النص بالاتجاه من اليمين لليسار / Check if RTL"""
    return get_text_direction() == "rtl"


def is_ltr() -> bool:
    """التحقق من أن النص بالاتجاه من اليسار لليمين / Check if LTR"""
    return get_text_direction() == "ltr"


# للاستخدام المباشر / For direct usage
__all__ = [
    "LanguageManager",
    "language_manager",
    "get_current_language",
    "set_current_language",
    "get_text_direction",
    "is_rtl",
    "is_ltr",
    "SUPPORTED_LANGUAGES",
    "DEFAULT_LANGUAGE"
]
