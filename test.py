"""
Tests and Validation
اختبار المشروع والتحقق من البيئة
"""

import sys
import os
from pathlib import Path


def test_imports():
    """Test if all required packages are installed"""
    print("🔍 Testing imports...")
    print("=" * 50)

    packages = {
        "customtkinter": "CustomTkinter (Modern UI)",
        "PIL": "Pillow (Image Processing)",
        "svgwrite": "SVGWrite (SVG Creation)",
        "cairosvg": "CairoSVG (SVG Conversion)",
        "rembg": "RemBG (Background Removal)",
    }

    all_ok = True
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {description:30} - OK")
        except ImportError as e:
            print(f"❌ {description:30} - MISSING")
            print(f"   Install with: pip install {package}")
            all_ok = False

    print("=" * 50)
    return all_ok


def test_directories():
    """Test if project structure is correct"""
    print("\n🗂️  Testing directory structure...")
    print("=" * 50)

    required_dirs = [
        "core",
        "ui",
        "assets",
        "assets/fonts",
        "assets/icons",
        "assets/templates",
        "exports",
    ]

    project_root = Path(__file__).parent
    all_ok = True

    for directory in required_dirs:
        dir_path = project_root / directory
        if dir_path.exists():
            print(f"✅ {directory:30} - EXISTS")
        else:
            print(f"❌ {directory:30} - MISSING")
            all_ok = False

    print("=" * 50)
    return all_ok


def test_files():
    """Test if all required files exist"""
    print("\n📄 Testing required files...")
    print("=" * 50)

    required_files = [
        "main.py",
        "config.py",
        "requirements.txt",
        "core/__init__.py",
        "core/icon_converter.py",
        "ui/__init__.py",
        "ui/main_window.py",
        "ui/icon_tab.py",
        "README.md",
        "README_AR.md",
    ]

    project_root = Path(__file__).parent
    all_ok = True

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✅ {file_path:30} - OK")
        else:
            print(f"❌ {file_path:30} - MISSING")
            all_ok = False

    print("=" * 50)
    return all_ok


def test_icon_converter():
    """Test IconConverter class"""
    print("\n⚙️  Testing IconConverter class...")
    print("=" * 50)

    try:
        from core.icon_converter import IconConverter
        print("✅ IconConverter imported successfully")

        # Test class attributes
        sizes = IconConverter.STANDARD_SIZES
        print(f"✅ Standard sizes defined: {len(sizes)} sizes")

        if len(sizes) > 0:
            print(f"   Sample sizes: {sizes[:3]}")

        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Error testing IconConverter: {e}")
        print("=" * 50)
        return False


def test_ui_components():
    """Test UI components can be imported"""
    print("\n🎨 Testing UI components...")
    print("=" * 50)

    try:
        from ui.main_window import MainWindow
        print("✅ MainWindow imported successfully")

        from ui.icon_tab import IconTab
        print("✅ IconTab imported successfully")

        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Error importing UI components: {e}")
        print("=" * 50)
        return False


def test_config():
    """Test configuration loading"""
    print("\n⚙️  Testing configuration...")
    print("=" * 50)

    try:
        import config
        print(f"✅ Config loaded: {config.APP_VERSION}")
        print(f"✅ Project root: {config.PROJECT_ROOT}")
        print(f"✅ Export directory: {config.EXPORTS_DIR}")
        print("=" * 50)
        return True
    except Exception as e:
        print(f"❌ Error loading config: {e}")
        print("=" * 50)
        return False


def main():
    """Run all tests"""
    print("""
╔════════════════════════════════════════════════════════╗
║   🧪 Iconora Studio - System Validation Test 🧪        ║
╚════════════════════════════════════════════════════════╝
    """)

    results = {
        "Imports": test_imports(),
        "Directories": test_directories(),
        "Files": test_files(),
        "IconConverter": test_icon_converter(),
        "UI Components": test_ui_components(),
        "Configuration": test_config(),
    }

    # Summary
    print("\n📊 TEST SUMMARY")
    print("=" * 50)

    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30} {status}")
        if not result:
            all_passed = False

    print("=" * 50)

    if all_passed:
        print("""
✨ All tests passed! Ready to launch! ✨
الآن جاهز للتشغيل! 🚀

Run the application with:
    python main.py
        """)
        return 0
    else:
        print("""
⚠️  Some tests failed. Please install missing dependencies:
    pip install -r requirements.txt
        """)
        return 1


if __name__ == "__main__":
    sys.exit(main())
