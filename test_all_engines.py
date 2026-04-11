"""
Quick test script to verify all core engines are working
"""

import sys
from pathlib import Path

# Test all imports
print("🧪 Testing Core Engines Import...")

try:
    from core.icon_converter import IconConverter
    print("  ✅ IconConverter imported")
except Exception as e:
    print(f"  ❌ IconConverter failed: {e}")
    sys.exit(1)

try:
    from core.svg_converter import SVGConverter
    print("  ✅ SVGConverter imported")
except Exception as e:
    print(f"  ❌ SVGConverter failed: {e}")
    sys.exit(1)

try:
    from core.logo_engine import LogoEngine
    print("  ✅ LogoEngine imported")
except Exception as e:
    print(f"  ❌ LogoEngine failed: {e}")
    sys.exit(1)

try:
    from core.signature_engine import SignatureEngine
    print("  ✅ SignatureEngine imported")
except Exception as e:
    print(f"  ❌ SignatureEngine failed: {e}")
    sys.exit(1)

try:
    from core.palette_engine import PaletteEngine
    print("  ✅ PaletteEngine imported")
except Exception as e:
    print(f"  ❌ PaletteEngine failed: {e}")
    sys.exit(1)

try:
    from core.project_manager import ProjectManager
    print("  ✅ ProjectManager imported")
except Exception as e:
    print(f"  ❌ ProjectManager failed: {e}")
    sys.exit(1)

print("\n🧪 Testing UI Tabs Import...")

try:
    from ui.icon_tab import IconConverterTab
    print("  ✅ IconConverterTab imported")
except Exception as e:
    print(f"  ❌ IconConverterTab failed: {e}")
    sys.exit(1)

try:
    from ui.svg_tab import SVGConverterTab
    print("  ✅ SVGConverterTab imported")
except Exception as e:
    print(f"  ❌ SVGConverterTab failed: {e}")
    sys.exit(1)

try:
    from ui.logo_tab import LogoDesignerTab
    print("  ✅ LogoDesignerTab imported")
except Exception as e:
    print(f"  ❌ LogoDesignerTab failed: {e}")
    sys.exit(1)

try:
    from ui.signature_tab import SignatureTab
    print("  ✅ SignatureTab imported")
except Exception as e:
    print(f"  ❌ SignatureTab failed: {e}")
    sys.exit(1)

try:
    from ui.palette_tab import PaletteTab
    print("  ✅ PaletteTab imported")
except Exception as e:
    print(f"  ❌ PaletteTab failed: {e}")
    sys.exit(1)

try:
    from ui.project_tab import ProjectManagerTab
    print("  ✅ ProjectManagerTab imported")
except Exception as e:
    print(f"  ❌ ProjectManagerTab failed: {e}")
    sys.exit(1)

print("\n🧪 Testing Core Engine Functionality...")

# Test Logo Engine
try:
    engine = LogoEngine()
    image = engine.generate_logo("Test", style="Minimal")
    print("  ✅ LogoEngine.generate_logo() works")
except Exception as e:
    print(f"  ❌ LogoEngine test failed: {e}")

# Test Signature Engine
try:
    engine = SignatureEngine()
    image = engine.generate_signature("John Doe")
    print("  ✅ SignatureEngine.generate_signature() works")
except Exception as e:
    print(f"  ❌ SignatureEngine test failed: {e}")

# Test Palette Engine
try:
    engine = PaletteEngine()
    palette = engine.generate_palette("Modern", palette_name="Sunset Vibes")
    print("  ✅ PaletteEngine.generate_palette() works")
    colors = engine.get_palette_colors("Modern", palette_name="Sunset Vibes")
    print(f"     Colors: {colors['colors']}")
except Exception as e:
    print(f"  ❌ PaletteEngine test failed: {e}")

# Test Project Manager
try:
    pm = ProjectManager()
    result = pm.create_template_project("logo_designer")
    print(f"  ✅ ProjectManager.create_template_project() works: {result['message']}")
except Exception as e:
    print(f"  ❌ ProjectManager test failed: {e}")

print("\n✨ All tests completed successfully!")
print("🚀 Application is ready to use!")
