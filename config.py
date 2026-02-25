"""
Configuration and Constants
المتغيرات الثابتة والإعدادات
"""

import os
from pathlib import Path

# ============================================================
# 🎨 Configuration Settings
# ============================================================

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Directories
EXPORTS_DIR = PROJECT_ROOT / "exports"
ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
ICONS_DIR = ASSETS_DIR / "icons"
TEMPLATES_DIR = ASSETS_DIR / "templates"

# Create directories if they don't exist
for directory in [EXPORTS_DIR, FONTS_DIR, ICONS_DIR, TEMPLATES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# ============================================================
# 🎨 UI Configuration
# ============================================================

# Window
WINDOW_TITLE = "Iconora Studio - أداة تحويل الأيقونات المحترفة"
WINDOW_SIZE = "1200x700"
WINDOW_MIN_SIZE = (900, 600)

# Theme
APPEARANCE_MODE = "dark"  # "dark" or "light"
COLOR_THEME = "blue"      # "blue", "green", "dark-blue"

# Fonts
FONT_PRIMARY = ("Arial", 12)
FONT_TITLE = ("Arial", 18, "bold")
FONT_SUBTITLE = ("Arial", 11)
FONT_SMALL = ("Arial", 10)

# Colors
COLOR_BG_PRIMARY = "#1a1a1a"
COLOR_BG_SECONDARY = "#252525"
COLOR_TEXT_PRIMARY = "#ffffff"
COLOR_TEXT_SECONDARY = "#888888"
COLOR_ACCENT = "#3498db"

# ============================================================
# 🖼️ Icon Configuration
# ============================================================

# Standard icon sizes
ICON_SIZES_STANDARD = [
    (16, 16),
    (24, 24),
    (32, 32),
    (48, 48),
    (64, 64),
    (128, 128),
    (256, 256),
]

# Icon size labels for UI
ICON_SIZES_LABELS = {
    (16, 16): "16x16 (Favicon)",
    (24, 24): "24x24 (Small)",
    (32, 32): "32x32 (Default)",
    (48, 48): "48x48 (Medium)",
    (64, 64): "64x64 (Large)",
    (128, 128): "128x128 (Extra Large)",
    (256, 256): "256x256 (Ultra Large)",
}

# Supported image formats
SUPPORTED_FORMATS = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif", "*.tiff")
IMAGE_FILTER = [("صور | Images", " ".join(SUPPORTED_FORMATS)), ("جميع الملفات | All", "*.*")]

# ============================================================
# 📊 Application Settings
# ============================================================

# Version
APP_VERSION = "1.0.0"
APP_PHASE = "Phase 1"

# Default export settings
DEFAULT_EXPORT_FORMAT = "ico"  # "ico" or "png"
AUTO_OPEN_EXPORT_FOLDER = False
SHOW_PREVIEW = True

# Quality settings
COMPRESSION_QUALITY = 95
INTERPOLATION_METHOD = "LANCZOS"  # For image resizing

# ============================================================
# 🌍 Localization
# ============================================================

# UI Labels (English & Arabic)
LABELS = {
    "app_title": "🎨 Iconora Studio",
    "app_subtitle": "أداة احترافية لتحويل الصور والتصميم",

    # Tabs
    "tab_icons": "تحويل الأيقونات | Icon Converter",
    "tab_svg": "قريباً - SVG | Soon - SVG",
    "tab_logos": "قريباً - الشعارات | Soon - Logos",

    # Buttons
    "btn_select_image": "📁 اختر صورة | Select Image",
    "btn_save_ico": "💾 حفظ كـ ICO | Save as ICO",
    "btn_save_png": "📸 حفظ PNG | Export PNG",

    # Messages
    "msg_select_image_first": "الرجاء اختيار صورة أولاً | Please select an image first",
    "msg_success": "تم بنجاح | Success!",
    "msg_error": "حدث خطأ | Error",
}

# ============================================================
# 🔧 Advanced Settings
# ============================================================

# Logging
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "app.log"

# Database (for future phases)
SAVE_PROJECT_FORMAT = ".iconora"  # Custom project format

# Debugging
DEBUG_MODE = False
VERBOSE_OUTPUT = False

print("[Config] Initialized successfully ✅")
