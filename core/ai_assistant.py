"""
Iconora Studio - AI Assistant Layer

Provides a unified interface for AI suggestions with:
- Primary provider: Ollama (Qwen2.5)
- Safe fallback logic when AI backend is unavailable
"""

from __future__ import annotations

import json
import os
import random
import re
import urllib.request
import urllib.error
from pathlib import Path

from config import ICONORA_DOCS


class AIAssistant:
    def __init__(
        self,
        endpoint: str | None = None,
        model: str | None = None,
        timeout: int | None = None,
    ):
        settings = self._load_local_settings()
        self.enabled = bool(settings.get("ai_enabled", True))
        self.endpoint = (
            endpoint
            or os.environ.get("ICONORA_AI_ENDPOINT")
            or settings.get("ai_endpoint")
            or "http://127.0.0.1:11434"
        ).rstrip("/")
        self.model = (
            model
            or os.environ.get("ICONORA_AI_MODEL")
            or settings.get("ai_model")
            or "qwen2.5:7b-instruct"
        )
        self.timeout = int(
            timeout
            or os.environ.get("ICONORA_AI_TIMEOUT")
            or settings.get("ai_timeout")
            or 30
        )

    @staticmethod
    def _load_local_settings() -> dict:
        settings_file = Path(ICONORA_DOCS) / "settings.json"
        if not settings_file.exists():
            return {}
        try:
            with open(settings_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception:
            return {}

    def _call_ollama(self, system_prompt: str, user_prompt: str, json_mode: bool = True) -> str:
        if not self.enabled:
            raise RuntimeError("AI assistant is disabled from settings")

        payload = {
            "model": self.model,
            "system": system_prompt,
            "prompt": user_prompt,
            "stream": False,
        }
        if json_mode:
            payload["format"] = "json"

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            f"{self.endpoint}/api/generate",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as response:
            body = response.read().decode("utf-8", errors="replace")
            parsed = json.loads(body)
            return parsed.get("response", "").strip()

    def is_backend_available(self) -> bool:
        if not self.enabled:
            return False
        try:
            req = urllib.request.Request(
                f"{self.endpoint}/api/tags",
                headers={"Content-Type": "application/json"},
                method="GET",
            )
            with urllib.request.urlopen(req, timeout=max(3, min(self.timeout, 10))):
                return True
        except Exception:
            return False

    @staticmethod
    def _extract_json_obj(text: str) -> dict:
        text = text.strip()
        if not text:
            return {}
        try:
            obj = json.loads(text)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass

        m = re.search(r"\{[\s\S]*\}", text)
        if not m:
            return {}
        try:
            obj = json.loads(m.group(0))
            return obj if isinstance(obj, dict) else {}
        except Exception:
            return {}

    @staticmethod
    def _sanitize_hex(value: str) -> str | None:
        if not isinstance(value, str):
            return None
        value = value.strip()
        if re.fullmatch(r"#?[0-9a-fA-F]{6}", value):
            return "#" + value.lstrip("#").upper()
        return None

    def suggest_logo(self, text: str, style: str = "modern", candidate_fonts: list[str] | None = None) -> dict:
        candidate_fonts = candidate_fonts or ["Arial", "Cairo", "Amiri", "Segoe UI"]
        fallback = {
            "text": text,
            "font": random.choice(candidate_fonts),
            "colors": ["#2563EB", "#60A5FA"],
            "layout": random.choice(["horizontal", "vertical", "stacked"]),
            "style": style,
        }

        system_prompt = (
            "You are a brand design assistant for an Arabic-first app. "
            "Return only valid JSON."
        )
        user_prompt = (
            f"Generate logo suggestions for text '{text}' with style '{style}'. "
            f"Use one font from: {candidate_fonts}. "
            "Return JSON with keys: font, colors (array of 2 hex), layout (horizontal|vertical|stacked), style."
        )

        try:
            raw = self._call_ollama(system_prompt, user_prompt, json_mode=True)
            data = self._extract_json_obj(raw)

            font = data.get("font") if data.get("font") in candidate_fonts else fallback["font"]
            colors = data.get("colors") if isinstance(data.get("colors"), list) else fallback["colors"]
            colors = [self._sanitize_hex(c) for c in colors[:2]]
            if len(colors) < 2 or any(c is None for c in colors):
                colors = fallback["colors"]

            layout = data.get("layout") if data.get("layout") in ["horizontal", "vertical", "stacked"] else fallback["layout"]
            out_style = data.get("style") if isinstance(data.get("style"), str) else style

            return {
                "text": text,
                "font": font,
                "colors": colors,
                "layout": layout,
                "style": out_style,
            }
        except Exception:
            return fallback

    def suggest_palette(self, description: str) -> dict:
        fallback_colors = [
            "#2563EB", "#60A5FA", "#A78BFA", "#F59E0B", "#10B981"
        ]

        system_prompt = (
            "You are a color assistant for UI/branding. "
            "Return only valid JSON."
        )
        user_prompt = (
            f"Create a 5-color palette for: '{description}'. "
            "Return JSON with keys: name, description, colors (array of 5 hex colors)."
        )

        try:
            raw = self._call_ollama(system_prompt, user_prompt, json_mode=True)
            data = self._extract_json_obj(raw)

            colors = data.get("colors") if isinstance(data.get("colors"), list) else []
            sanitized = []
            for color in colors:
                hx = self._sanitize_hex(color)
                if hx:
                    sanitized.append(hx)
                if len(sanitized) == 5:
                    break

            if len(sanitized) < 5:
                sanitized = fallback_colors

            return {
                "name": data.get("name") if isinstance(data.get("name"), str) and data.get("name").strip() else description,
                "description": data.get("description") if isinstance(data.get("description"), str) else f"AI Generated for: {description}",
                "colors": sanitized,
            }
        except Exception:
            return {
                "name": description,
                "description": f"AI Generated (fallback) for: {description}",
                "colors": fallback_colors,
            }
