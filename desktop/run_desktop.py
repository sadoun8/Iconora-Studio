from __future__ import annotations

import argparse
import ctypes
import os
import socket
import sys
import threading
import time
import traceback
import urllib.request
from datetime import datetime
from pathlib import Path

import uvicorn
import webview


ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


LOG_DIR = Path.home() / "Documents" / "Iconora Studio" / "Logs"
DESKTOP_LOG = LOG_DIR / "desktop_shell.log"


def _log(message: str) -> None:
    try:
        LOG_DIR.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(DESKTOP_LOG, "a", encoding="utf-8") as handle:
            handle.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass


def _show_message(title: str, message: str) -> None:
    ctypes.windll.user32.MessageBoxW(0, message, title, 0x10)


def _pick_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def _has_webview2_runtime() -> bool:
    program_files = [
        os.environ.get("ProgramFiles(x86)", ""),
        os.environ.get("ProgramFiles", ""),
    ]
    for base in program_files:
        candidate = Path(base) / "Microsoft" / "EdgeWebView" / "Application"
        if candidate.exists():
            return True
    return False


class BackendRunner:
    def __init__(self, port: int) -> None:
        self.port = port
        self.server: uvicorn.Server | None = None
        self.thread: threading.Thread | None = None
        self.startup_error: str | None = None
        self.started_at: float = 0.0

    def _run_server(self) -> None:
        try:
            _log("Backend thread started.")
            import_started = time.time()
            from backend.main import app
            _log(f"Imported backend.main in {time.time() - import_started:.2f}s.")

            config = uvicorn.Config(
                app,
                host="127.0.0.1",
                port=self.port,
                log_level="info",
            )
            self.server = uvicorn.Server(config)
            _log(f"Starting Uvicorn on 127.0.0.1:{self.port}.")
            self.server.run()
        except Exception:
            self.startup_error = traceback.format_exc()
            _log(f"Backend startup error:\n{self.startup_error}")

    def start(self) -> None:
        os.environ["ICONORA_DESKTOP_MODE"] = "1"
        self.started_at = time.time()
        _log(f"Launching backend on port {self.port}.")
        self.thread = threading.Thread(target=self._run_server, daemon=True)
        self.thread.start()

    def wait_until_ready(self, timeout: float = 120.0) -> bool:
        deadline = time.time() + timeout
        health_url = f"http://127.0.0.1:{self.port}/api/health"
        while time.time() < deadline:
            if self.startup_error:
                return False
            try:
                with urllib.request.urlopen(health_url, timeout=2):
                    _log(f"Backend health check succeeded after {time.time() - self.started_at:.2f}s.")
                    return True
            except Exception:
                time.sleep(0.25)
        _log(f"Backend health check timed out after {timeout:.0f}s.")
        return False

    def stop(self) -> None:
        if self.server is not None:
            self.server.should_exit = True
        if self.thread is not None:
            self.thread.join(timeout=5)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dev", action="store_true", help="Use Vite dev server for the UI")
    args = parser.parse_args()
    _log("Desktop shell launched.")

    if not _has_webview2_runtime():
        _log("WebView2 runtime not found.")
        _show_message(
            "Iconora Studio",
            "Microsoft Edge WebView2 Runtime is required to run the desktop shell.",
        )
        return 1

    port = _pick_port()
    backend = BackendRunner(port)
    backend.start()

    if not backend.wait_until_ready():
        backend.stop()
        if backend.startup_error:
            print(backend.startup_error, file=sys.stderr)
            _show_message(
                "Iconora Studio",
                f"Backend failed to start. Check the log:\n{DESKTOP_LOG}",
            )
        else:
            _show_message(
                "Iconora Studio",
                f"Backend failed to start in time. Check the log:\n{DESKTOP_LOG}",
            )
        return 1

    target_url = "http://localhost:5173" if args.dev else f"http://127.0.0.1:{port}"
    _log(f"Opening window at {target_url}.")

    window = webview.create_window("Iconora Studio", target_url, width=1440, height=960)
    window.events.closed += lambda: backend.stop()
    webview.start(debug=args.dev, gui="edgechromium")
    _log("Desktop shell exited cleanly.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
