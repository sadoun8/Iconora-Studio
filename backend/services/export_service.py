from __future__ import annotations

import base64
import tempfile
from io import BytesIO
from pathlib import Path

from PIL import Image

from config import EXPORT_SUBDIRS


FORMAT_TO_DIR = {
    "png": EXPORT_SUBDIRS["Logos"],
    "webp": EXPORT_SUBDIRS["Logos"],
    "pdf": EXPORT_SUBDIRS["Logos"],
    "ico": EXPORT_SUBDIRS["Icons"],
    "svg": EXPORT_SUBDIRS["SVGs"],
}


def _decode_data_url(data_url: str) -> Image.Image:
    if not data_url or "," not in data_url:
        raise ValueError("Missing or invalid data URL")
    _, encoded = data_url.split(",", 1)
    data = base64.b64decode(encoded)
    image = Image.open(BytesIO(data))
    if image.mode != "RGBA":
        image = image.convert("RGBA")
    return image


def _sanitize_filename(name: str | None, ext: str) -> str:
    stem = (name or f"iconora_export.{ext}").rsplit(".", 1)[0]
    safe = "".join(ch if ch.isalnum() or ch in {"_", "-"} else "_" for ch in stem).strip("_")
    safe = safe or "iconora_export"
    return f"{safe}.{ext}"


def export_canvas(
    data_url: str,
    export_format: str,
    filename: str | None = None,
    svg_text: str | None = None,
) -> tuple[str, list[str]]:
    export_dir = FORMAT_TO_DIR[export_format]
    export_dir.mkdir(parents=True, exist_ok=True)
    output_path = export_dir / _sanitize_filename(filename, export_format)
    warnings: list[str] = []

    if export_format == "svg":
        if not svg_text:
            raise ValueError("Missing SVG payload")
        output_path.write_text(svg_text, encoding="utf-8")
        return str(output_path), warnings

    image = _decode_data_url(data_url)
    if export_format == "png":
        image.save(output_path, "PNG", optimize=True)
    elif export_format == "webp":
        image.save(output_path, "WEBP", quality=90, lossless=True)
    elif export_format == "pdf":
        image.convert("RGB").save(output_path, "PDF", resolution=300.0)
    elif export_format == "ico":
        sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
        image.save(output_path, "ICO", sizes=sizes)
    else:
        raise ValueError(f"Unsupported export format: {export_format}")
    return str(output_path), warnings


def export_icon_pack(data_url: str, filename: str | None = None) -> tuple[str, list[str], list[str]]:
    from core.icon_converter import IconConverter

    icon_name = _sanitize_filename(filename, "ico")
    icon_path = EXPORT_SUBDIRS["Icons"] / icon_name
    EXPORT_SUBDIRS["Icons"].mkdir(parents=True, exist_ok=True)
    image = _decode_data_url(data_url)
    warnings: list[str] = []
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as handle:
        temp_path = Path(handle.name)
    try:
        image.save(temp_path, "PNG", optimize=True)
        converter = IconConverter(str(temp_path))
        output_path, large_paths = converter.convert_to_ico(str(icon_path))
    finally:
        temp_path.unlink(missing_ok=True)
    return output_path, large_paths, warnings
