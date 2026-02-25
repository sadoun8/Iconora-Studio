#!/usr/bin/env python3
"""
Logo Design Testing & Examples
اختبار وأمثلة محرك تصميم الشعارات

Quick start guide and testing examples for the Logo Engine
"""

print("=" * 70)
print("🎨 Iconora Studio - Phase 3: Logo Designer Testing")
print("=" * 70)

# Test 1: Module imports
print("\n✅ Test 1: Importing modules...")
try:
    from core.logo_engine import LogoEngine, GradientGenerator
    from PIL import Image
    print("   ✓ LogoEngine imported successfully")
    print("   ✓ GradientGenerator imported successfully")
except Exception as e:
    print(f"   ✗ Import error: {e}")
    exit(1)

# Test 2: Initialize engine
print("\n✅ Test 2: Initializing LogoEngine...")
try:
    engine = LogoEngine()
    print(f"   ✓ Engine initialized")
    print(f"   ✓ Export folder: {engine.export_folder}")
except Exception as e:
    print(f"   ✗ Error: {e}")
    exit(1)

# Test 3: Get system fonts
print("\n✅ Test 3: Scanning system fonts...")
try:
    fonts = engine.get_system_fonts()
    font_list = list(fonts.keys())[:5]
    print(f"   ✓ Found {len(fonts)} fonts on system")
    print(f"   ✓ First 5 fonts: {', '.join(font_list)}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 4: Create simple logo
print("\n✅ Test 4: Creating simple logo...")
try:
    success, msg, path = engine.generate_logo(
        text="Test Logo",
        font_name="arial.ttf",
        font_size=80,
        text_color="#FFFFFF",
        bg_color="#0066FF"
    )

    if success:
        print(f"   ✓ Logo created: {msg}")
        print(f"   ✓ File: {path}")

        # Check file exists
        import os
        if os.path.exists(path):
            size = os.path.getsize(path) / 1024
            print(f"   ✓ File size: {size:.1f} KB")
        else:
            print(f"   ✗ File not found")
    else:
        print(f"   ✗ Error: {msg}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 5: Create logo with gradient
print("\n✅ Test 5: Creating logo with gradient...")
try:
    success, msg, path = engine.generate_logo(
        text="Gradient Logo",
        font_size=90,
        text_color="#FFFFFF",
        bg_color="#FF6B6B",
        use_gradient=True,
        gradient_color2="#1E90FF",
        gradient_direction="diagonal",
        effects={"shadow": True}
    )

    if success:
        print(f"   ✓ Gradient logo created: {msg}")
    else:
        print(f"   ✗ Error: {msg}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 6: Batch generation
print("\n✅ Test 6: Batch logo generation...")
try:
    logos_data = [
        {
            "text": "Company A",
            "font_size": 80,
            "text_color": "#FFFFFF",
            "bg_color": "#003366",
            "effects": {"shadow": True}
        },
        {
            "text": "Company B",
            "font_size": 80,
            "text_color": "#FFFFFF",
            "bg_color": "#FF6B6B",
            "use_gradient": True,
            "gradient_color2": "#FF9933"
        },
    ]

    results = engine.batch_generate_logos(logos_data)

    print(f"   ✓ Batch generation completed")
    print(f"   ✓ Successfully created: {len(results['success'])} logos")
    print(f"   ✗ Failed: {len(results['failed'])} logos")

    for item in results['success']:
        print(f"      • {item['text']}: {item['path']}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 7: Resize logo
print("\n✅ Test 7: Testing logo resizing...")
try:
    success, msg, path = engine.generate_logo(
        text="Resize Test",
        font_size=80,
        text_color="#000000",
        bg_color="#FFFF00"
    )

    if success:
        resized = engine.resize_logo(path, 400, 200)
        print(f"   ✓ Logo resized: {resized}")
    else:
        print(f"   ✗ Error: {msg}")
except Exception as e:
    print(f"   ✗ Error: {e}")

# Test 8: Color conversion
print("\n✅ Test 8: Testing color conversion...")
try:
    color1 = GradientGenerator.hex_to_rgba("#FFFFFF", 255)
    color2 = GradientGenerator.hex_to_rgba("#FF6B6B", 200)
    print(f"   ✓ White: {color1}")
    print(f"   ✓ Red (200 alpha): {color2}")
except Exception as e:
    print(f"   ✗ Error: {e}")

print("\n" + "=" * 70)
print("🎉 All tests completed!")
print("=" * 70)
print("\n📂 Generated logos are saved in: exports/")
print("🎨 Next step: Run 'python main.py' to launch the GUI\n")
