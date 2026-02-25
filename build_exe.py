"""
Build Script for Iconora Studio
Script to build executable file (.exe)

Usage:
    python build_exe.py
"""

import os
import sys
import subprocess
from pathlib import Path


def build_exe():
    """Build Iconora Studio as executable"""

    print("🔨 Building Iconora Studio...")
    print("=" * 50)

    project_root = Path(__file__).parent

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("❌ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])

    # Build command
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onefile",                      # Single executable
        "--windowed",                     # No console window
        "--name=IconoraStudio",           # App name
        "--icon=assets/icons/app.ico",    # Icon (optional)
        "--add-data=assets:assets",       # Include assets
        "main.py"
    ]

    try:
        subprocess.check_call(cmd)
        print("\n✅ Build completed successfully!")
        print(f"📦 Executable location: {project_root / 'dist' / 'IconoraStudio.exe'}")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")
        return False

    return True


if __name__ == "__main__":
    build_exe()
