"""
Iconora Studio - Configuration and Constants
الإعدادات والثوابت
"""

import os
import tempfile
from pathlib import Path

# ============================================================
# 📁 Path Configuration
# ============================================================

# Project root directory
PROJECT_ROOT = Path(__file__).parent

# Standard export path in user documents with a writable fallback.
USER_DOCS = Path(os.path.expanduser("~/Documents"))


def _is_directory_writable(directory: Path) -> bool:
    """Return True when the directory can be created and written to."""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=directory, prefix=".iconora_probe_", delete=True) as probe:
            probe.write(b"ok")
            probe.flush()
        return True
    except Exception:
        return False


def _resolve_data_root() -> Path:
    """Pick the first writable application data directory."""
    candidates = [
        USER_DOCS / "Iconora Studio",
        Path(os.environ.get("LOCALAPPDATA", "")) / "Iconora Studio" if os.environ.get("LOCALAPPDATA") else None,
        PROJECT_ROOT / ".iconora-data",
    ]
    for candidate in candidates:
        if candidate and _is_directory_writable(candidate):
            return candidate
    fallback = PROJECT_ROOT / ".iconora-data"
    fallback.mkdir(parents=True, exist_ok=True)
    return fallback


ICONORA_DOCS = _resolve_data_root()
EXPORTS_DIR = ICONORA_DOCS / "Exports"
PROJECTS_DIR = ICONORA_DOCS / "Projects"
LOG_DIR = ICONORA_DOCS / "Logs"

# Category-specific export directories
EXPORT_SUBDIRS = {
    "Icons": EXPORTS_DIR / "Icons",
    "SVGs": EXPORTS_DIR / "SVGs",
    "Logos": EXPORTS_DIR / "Logos",
    "Signatures": EXPORTS_DIR / "Signatures",
    "Palettes": EXPORTS_DIR / "Palettes"
}

# Assets
ASSETS_DIR = PROJECT_ROOT / "assets"
FONTS_DIR = ASSETS_DIR / "fonts"
ICONS_DIR = ASSETS_DIR / "icons"
TEMPLATES_DIR = ASSETS_DIR / "templates"

# Create all necessary directories
ALL_DIRS = [ICONORA_DOCS, EXPORTS_DIR, PROJECTS_DIR, LOG_DIR, FONTS_DIR, ICONS_DIR, TEMPLATES_DIR] + list(EXPORT_SUBDIRS.values())

for directory in ALL_DIRS:
    try:
        directory.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Warning: Could not create directory {directory}: {e}")

# ============================================================
# 🎨 UI Configuration
# ============================================================

WINDOW_TITLE = "Iconora Studio - Professional Design Suite"
WINDOW_SIZE = "1200x800"
WINDOW_MIN_SIZE = (1000, 700)

# Theme
APPEARANCE_MODE = "dark"
COLOR_THEME = "blue"

# Colors (Modern Palette)
COLOR_BG_PRIMARY = ["#F1F5F9", "#0F0F0F"]
COLOR_BG_SECONDARY = ["#FFFFFF", "#1A1A1A"]
COLOR_ACCENT = ["#667EEA", "#764BA2"]

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
    (512, 512)
]

# Supported image formats
SUPPORTED_FORMATS = ("*.png", "*.jpg", "*.jpeg", "*.bmp", "*.gif")

# ============================================================
# 📊 Application Settings
# ============================================================

APP_VERSION = "2.0.0"
APP_PHASE = "Professional Edition"

# Default export settings
DEFAULT_EXPORT_FORMAT = "ico"
AUTO_OPEN_EXPORT_FOLDER = False
SHOW_PREVIEW = True

# Logging
ENABLE_LOGGING = True
LOG_LEVEL = "INFO"
LOG_FILE = LOG_DIR / "app.log"

print(f"[Config] Initialized successfully. Data root: {ICONORA_DOCS}")
