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

    print("Building Iconora Studio...")
    print("=" * 50)

    project_root = Path(__file__).parent
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    # Cleanup old builds
    import shutil
    if dist_dir.exists():
        print(f"Cleaning {dist_dir}...")
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        print(f"Cleaning {build_dir}...")
        shutil.rmtree(build_dir)

    # Check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])

    # Build command - using one-dir mode for better DLL handling
    cmd = [
        sys.executable,
        "-m", "PyInstaller",
        "--onedir",                       # One-dir bundle (better for DLL handling)
        "--windowed",                     # No console window
        "--name=Iconora Studio",          # App name (must match installer expectations)
        "--collect-all=tkinter",          # Collect all tkinter files
        "--collect-all=PIL",              # Include PIL/Pillow completely
        "--collect-all=customtkinter",    # Include customtkinter completely
        "--collect-all=cairosvg",         # Include cairosvg package data (VERSION file, etc.)
        "--add-data=assets;assets",       # Add assets folder
        "--add-data=ui;ui",               # Add ui package
        "--add-data=core;core",           # Add core package
        "--distpath=dist",                # Output directory
        "--workpath=build",               # Build directory
        "--specpath=.",                   # Spec file directory
        "--hidden-import=customtkinter",  # Hidden imports
        "--hidden-import=PIL",
        "--hidden-import=tkinterdnd2",
        "--hidden-import=cairosvg",
        "--hidden-import=rembg",
        "main.py"
    ]

    try:
        subprocess.check_call(cmd)
        print("\nBuild completed successfully!")

        # Copy assets and ui packages to _internal folder (PyInstaller limitation workaround)
        for folder in ["assets", "ui", "core"]:
            src = project_root / folder
            dst = project_root / "dist" / "Iconora Studio" / "_internal" / folder
            if src.exists():
                import shutil
                if dst.exists():
                    shutil.rmtree(dst)
                shutil.copytree(src, dst)
                print(f"Copied {folder} package to {dst}")

        print(f"Executable location: {project_root / 'dist' / 'Iconora Studio' / 'Iconora Studio.exe'}")
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        return False

    return True


if __name__ == "__main__":
    if build_exe():
        sys.exit(0)
    else:
        sys.exit(1)
