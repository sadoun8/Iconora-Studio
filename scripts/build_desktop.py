from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"
MINOR_VERSION_LIMIT = 14


def ensure_pyinstaller() -> None:
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PyInstaller"])


def ensure_runtime_dependencies() -> None:
    if sys.version_info.major == 3 and sys.version_info.minor >= MINOR_VERSION_LIMIT:
        raise RuntimeError(
            "Desktop packaging currently requires Python 3.13 or older. "
            "The active interpreter is Python "
            f"{sys.version_info.major}.{sys.version_info.minor}, and pywebview "
            "cannot be installed reliably on this runtime yet."
        )

    required_modules = {
        "webview": "pywebview",
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "PIL": "pillow",
    }

    missing_packages = []
    for module_name, package_name in required_modules.items():
        try:
            __import__(module_name)
        except ImportError:
            missing_packages.append(package_name)

    if missing_packages:
        package_list = ", ".join(missing_packages)
        print(f"Installing missing desktop dependencies: {package_list}")
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", *missing_packages],
        )


def main() -> int:
    ensure_pyinstaller()
    try:
        ensure_runtime_dependencies()
    except RuntimeError as exc:
        print(f"Desktop build blocked: {exc}")
        return 1
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--clean",
        "--onedir",
        "--windowed",
        "--name=Iconora Studio",
        "--icon=assets/icons/app.ico",
        "--add-data=assets;assets",
        "--add-data=backend;backend",
        "--add-data=core;core",
        "--add-data=frontend;frontend",
        "--hidden-import=webview",
        "--hidden-import=uvicorn",
        "--hidden-import=fastapi",
        "--hidden-import=PIL",
        "--collect-all=PIL",
        "--collect-all=webview",
        "desktop/run_desktop.py",
    ]
    subprocess.check_call(command, cwd=str(ROOT))
    print(f"Desktop build complete: {DIST_DIR / 'Iconora Studio'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
