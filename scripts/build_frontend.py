from __future__ import annotations

import shutil
import subprocess
import sys
from shutil import which
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"
BACKEND_STATIC_DIR = ROOT / "backend" / "static"


def resolve_npm() -> str:
    candidates = ["npm.cmd", "npm"] if sys.platform.startswith("win") else ["npm"]
    for candidate in candidates:
        found = which(candidate)
        if found:
            return found
    raise FileNotFoundError(
        "npm was not found on PATH. Install Node.js and ensure npm is available in the current shell."
    )


def run(command: list[str], cwd: Path) -> None:
    if sys.platform.startswith("win"):
        subprocess.check_call(
            [
                "powershell.exe",
                "-NoProfile",
                "-Command",
                f"& {subprocess.list2cmdline(command)}",
            ],
            cwd=str(cwd),
        )
    else:
        subprocess.check_call(command, cwd=str(cwd))


def main() -> int:
    npm = resolve_npm()
    BACKEND_STATIC_DIR.mkdir(parents=True, exist_ok=True)

    node_modules_dir = FRONTEND_DIR / "node_modules"
    package_lock = FRONTEND_DIR / "package-lock.json"

    if not node_modules_dir.exists():
        install_command = [npm, "ci"] if package_lock.exists() else [npm, "install"]
        run(install_command, FRONTEND_DIR)
    else:
        print("Using existing frontend dependencies from node_modules")

    vite_bin = FRONTEND_DIR / "node_modules" / ".bin" / ("vite.cmd" if sys.platform.startswith("win") else "vite")
    if vite_bin.exists():
        run([str(vite_bin), "build"], FRONTEND_DIR)
    else:
        run([npm, "run", "build"], FRONTEND_DIR)

    dist_dir = FRONTEND_DIR / "dist"
    if not dist_dir.exists():
        raise FileNotFoundError("frontend/dist was not generated")

    if BACKEND_STATIC_DIR.exists():
        shutil.rmtree(BACKEND_STATIC_DIR)
    shutil.copytree(dist_dir, BACKEND_STATIC_DIR)
    print(f"Copied frontend build to {BACKEND_STATIC_DIR}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
