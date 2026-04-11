---
description: Repository Information Overview
alwaysApply: true
---

# Iconora Studio Information

## Summary
**Iconora Studio** is a professional Windows desktop application for image conversion and design. It provides a comprehensive suite for creating icons, converting images to SVG, and designing professional logos. The application features a modern UI with full **Arabic (RTL) and English (LTR)** support, including 200+ localized strings.

## Structure
- **core/**: Contains processing engines (Icon Converter, SVG Converter, Logo Engine).
- **ui/**: Contains CustomTkinter-based interface components (Main Window, Icon Tab, SVG Tab, Logo Tab).
- **assets/**: Static resources including custom fonts, app icons, and templates.
- **installers/**: Configuration and scripts for building Windows installers using Inno Setup.
- **exports/**: Default output directory for converted images and designed logos.

## Language & Runtime
**Language**: Python  
**Version**: 3.10+ (Tested on 3.11/3.12)  
**Build System**: PyInstaller (for executable) & Inno Setup (for installer)  
**Package Manager**: pip (requirements.txt)

## Dependencies
**Main Dependencies**:
- `customtkinter==5.2.2`: Modern UI framework.
- `pillow==10.1.0`: Advanced image processing.
- `svgwrite==1.4.3`: SVG generation.
- `cairosvg==2.7.1`: SVG conversion and rendering.
- `rembg==2.0.60`: AI-powered background removal.
- `PyInstaller==6.4.0`: Executable packaging.
- `tkinterdnd2==0.3.0`: Drag and drop support.

**Development Dependencies**:
- `pytest>=7.4.4`: Testing framework.
- `black`, `flake8`, `pylint`: Code quality and formatting.

## Build & Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python main.py

# Build standalone executable (.exe)
python build_exe.py

# Build Windows Installer (requires Inno Setup)
powershell ./installers/build_installer.ps1
```

## Main Files & Resources
- **main.py**: Primary entry point for the application.
- **config.py**: Global configuration, theme settings, and constants.
- **i18n.py**: Localization system for Arabic and English support.
- **core/logo_engine.py**: Advanced engine for logo design with gradients and effects.
- **core/icon_converter.py**: Logic for multi-size ICO generation.
- **ui/main_window.py**: Main UI container with dynamic tab management.

## Testing
**Framework**: custom `test.py` runner and `pytest`.
**Test Location**: Root directory (`test*.py`).
**Naming Convention**: `test_*.py` and `integration_test.py`.
**Configuration**: Handled within test scripts and `config.py`.

**Run Command**:
```bash
# Basic environment and structure validation
python test.py

# Specific module tests (e.g., Logo Engine)
python test_logo_engine.py

# Integration tests
python integration_test.py
```
