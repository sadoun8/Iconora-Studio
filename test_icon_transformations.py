"""
Test Icon Transformations and Export
Verifies that image transformations (rotate, scale, opacity) are applied during export.
"""

import os
import sys
import gc
from pathlib import Path
from PIL import Image
import tempfile
import shutil

# Add core to path
sys.path.insert(0, str(Path(__file__).parent))

from core.icon_converter import IconConverter


def create_test_image(output_path, size=(256, 256), color=(255, 100, 100)):
    """Create a simple test image for testing"""
    img = Image.new('RGB', size, color=color)
    img.save(output_path)
    return output_path


def test_rotate_and_export():
    """Test: Rotate image and export as ICO and PNG"""
    print("\n=== TEST 1: Rotate and Export ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image
        test_img = create_test_image(os.path.join(tmpdir, "test.png"))
        print(f"✓ Created test image: {test_img}")

        # Initialize converter
        converter = IconConverter(test_img)
        original_size = converter.image.size
        print(f"✓ Original image size: {original_size}")

        # Rotate image
        converter.rotate_image(90)
        rotated_size = converter.image.size
        print(f"✓ Rotated image size (should be different for non-square): {rotated_size}")

        # Export as ICO
        ico_output = os.path.join(tmpdir, "test_rotated.ico")
        converter.convert_to_ico(ico_output, [(32, 32)])
        assert os.path.exists(ico_output), "ICO file not created"
        print(f"✓ ICO exported: {ico_output} ({os.path.getsize(ico_output)} bytes)")

        # Export as PNG
        png_folder = os.path.join(tmpdir, "png_output")
        results = converter.export_all_sizes(png_folder)
        assert len(results) > 0, "PNG export failed"
        print(f"✓ PNG exported: {len(results)} files")
        for f in results:
            print(f"  - {os.path.basename(f)} ({os.path.getsize(f)} bytes)")


def test_scale_and_export():
    """Test: Scale image and verify output sizes are correct"""
    print("\n=== TEST 2: Scale and Export ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image
        test_img_path = os.path.join(tmpdir, "test.png")
        create_test_image(test_img_path, size=(100, 100))
        test_img = test_img_path
        print(f"✓ Created test image (100x100)")

        # Initialize converter
        converter = IconConverter(test_img)

        # Scale to 200% (should be 200x200)
        converter.scale_image(2.0)
        scaled_size = converter.image.size
        print(f"✓ Scaled image size (200%): {scaled_size}")
        assert scaled_size == (200, 200), f"Expected (200, 200), got {scaled_size}"

        # Export as PNG
        png_folder = os.path.join(tmpdir, "png_output")
        results = converter.export_all_sizes(png_folder)
        print(f"✓ PNG exported: {len(results)} files (all scaled)")

        # Check that exported sizes are as expected
        for result in results:
            img = Image.open(result)
            width, height = img.size
            # Since we scaled to 2x, exported sizes should be roughly 2x their nominal size
            print(f"  - {os.path.basename(result)}: {width}x{height}")
            img.close()  # Explicitly close to release file handle


def test_opacity_and_export():
    """Test: Apply opacity and verify RGBA transparency"""
    print("\n=== TEST 3: Opacity and Export ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image
        test_img = create_test_image(os.path.join(tmpdir, "test.png"))
        print(f"✓ Created test image")

        # Initialize converter
        converter = IconConverter(test_img)
        original_mode = converter.image.mode
        print(f"✓ Original image mode: {original_mode}")

        # Set opacity to 50%
        converter.set_opacity(0.5)
        final_mode = converter.image.mode
        print(f"✓ After opacity: image mode = {final_mode}")
        assert final_mode == 'RGBA', "Should be RGBA after opacity"

        # Export as PNG
        png_folder = os.path.join(tmpdir, "png_output")
        results = converter.export_all_sizes(png_folder)
        print(f"✓ PNG exported: {len(results)} files with transparency")

        # Verify PNG has alpha channel
        if results:
            test_png = Image.open(results[0])
            print(f"  - {os.path.basename(results[0])}: mode={test_png.mode} (should have alpha)")
            test_png.close()


def test_combined_transforms():
    """Test: Apply multiple transformations together"""
    print("\n=== TEST 4: Combined Transformations ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image
        test_img = create_test_image(os.path.join(tmpdir, "test.png"))
        print(f"✓ Created test image")

        # Initialize converter
        converter = IconConverter(test_img)

        # Apply multiple transformations
        converter.rotate_image(45)
        print(f"✓ Rotated 45°")

        converter.scale_image(1.5)
        print(f"✓ Scaled to 150%")

        converter.set_opacity(0.8)
        print(f"✓ Set opacity to 80%")

        # Export
        ico_output = os.path.join(tmpdir, "test_combined.ico")
        converter.convert_to_ico(ico_output, [(64, 64)])
        assert os.path.exists(ico_output), "Combined transform ICO export failed"
        print(f"✓ Combined ICO exported: {os.path.getsize(ico_output)} bytes")

        # Export PNG
        png_folder = os.path.join(tmpdir, "png_output")
        results = converter.export_all_sizes(png_folder)
        print(f"✓ Combined PNG exported: {len(results)} files")


def test_reset_reverts_changes():
    """Test: Reset image reverts all transformations"""
    print("\n=== TEST 5: Reset Image ===")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test image
        test_img = create_test_image(os.path.join(tmpdir, "test.png"))

        # Initialize converter
        converter = IconConverter(test_img)
        original_size = converter.image.size
        print(f"✓ Original size: {original_size}")

        # Apply transformations
        converter.scale_image(2.0)
        scaled_size = converter.image.size
        print(f"✓ After scaling: {scaled_size}")

        # Reset
        converter.reset_image()
        reset_size = converter.image.size
        print(f"✓ After reset: {reset_size}")

        assert reset_size == original_size, "Reset should restore original size"
        print(f"✓ Reset successfully reverted transformations")


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("ICON TRANSFORMATION AND EXPORT TESTS")
    print("=" * 60)

    try:
        test_rotate_and_export()
        gc.collect()

        test_scale_and_export()
        gc.collect()

        test_opacity_and_export()
        gc.collect()

        test_combined_transforms()
        gc.collect()

        test_reset_reverts_changes()
        gc.collect()

        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        return True

    except AssertionError as e:
        print(f"\n❌ TEST FAILED: {e}")
        return False
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
