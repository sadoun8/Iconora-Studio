"""
Build a portable ZIP installer for Iconora Studio
Run this after PyInstaller builds to dist/Iconora Studio
"""
import shutil
import os
from pathlib import Path
from datetime import datetime

def build_portable_installer():
    """Create a portable ZIP installer"""

    # Paths
    root = Path(__file__).parent.parent
    dist_app = root / "dist" / "Iconora Studio"
    output_dir = root / "installers" / "Output"

    if not dist_app.exists():
        print(f"❌ Error: {dist_app} not found")
        print("   Run: python -m PyInstaller 'Iconora Studio.spec' --clean")
        return False

    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)

    # Create ZIP
    zip_name = f"Iconora-Studio-{datetime.now().strftime('%Y%m%d-%H%M%S')}-Portable"
    zip_path = output_dir / zip_name

    print(f"📦 Creating portable installer...")
    print(f"   Source: {dist_app}")
    print(f"   Output: {zip_path}.zip")

    try:
        # Create ZIP archive
        shutil.make_archive(str(zip_path), 'zip', dist_app.parent, "Iconora Studio")

        print(f"✅ Portable installer created: {zip_path}.zip")
        print(f"\n📋 Installation instructions:")
        print(f"   1. Extract ZIP to desired location")
        print(f"   2. Run: Iconora Studio.exe")
        print(f"\n📂 File size: {(zip_path.with_suffix('.zip').stat().st_size / 1024 / 1024):.2f} MB")

        return True

    except Exception as e:
        print(f"❌ Error creating ZIP: {e}")
        return False

if __name__ == "__main__":
    build_portable_installer()
