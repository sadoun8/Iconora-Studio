"""
Iconora Studio - Icon Converter Engine (v2.0)
Supports up to 4096px, text overlays, borders, backgrounds, and batch export.
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageChops, ImageEnhance

try:
    from rembg import remove
    HAS_REMBG = True
except ImportError:
    remove = None
    HAS_REMBG = False

import os
import re
from pathlib import Path

class IconConverter:
    """Professional icon conversion with extensive modification tools"""

    STANDARD_SIZES = [
        (16, 16), (24, 24), (32, 32), (48, 48),
        (64, 64), (128, 128), (256, 256), (512, 512),
        (1024, 1024), (2048, 2048), (4096, 4096)
    ]

    def __init__(self, image_path: str):
        self.image_path = image_path
        self.original_image: Image.Image | None = None
        self.working_image: Image.Image | None = None
        self.load_image()

    @property
    def image(self) -> Image.Image:
        """Backward-compatible alias for working_image."""
        return self.working_image

    @image.setter
    def image(self, value: Image.Image):
        self.working_image = value

    # ─── Loading ──────────────────────────────────────────────
    def load_image(self):
        img = Image.open(self.image_path)
        if img.mode != 'RGBA':
            img = img.convert('RGBA')
        self.original_image = img.copy()
        self.working_image  = img.copy()

    def reset_image(self):
        self.working_image = self.original_image.copy()

    def remove_background(self):
        """Remove background using AI (rembg)"""
        if not HAS_REMBG:
            raise ImportError("rembg is not installed. Install with `pip install rembg` to enable background removal.")
        if self.working_image:
            self.working_image = remove(self.working_image)
            # Update original so reset doesn't bring back BG?
            # Or keep original as-is. Let's keep original for full reset.

    def get_image_copy(self) -> Image.Image:
        return self.working_image.copy()

    # ─── Transforms ───────────────────────────────────────────
    def rotate_image(self, degrees: float):
        self.working_image = self.working_image.rotate(-degrees, expand=True)

    def scale_image(self, factor: float):
        w, h = self.working_image.size
        self.working_image = self.working_image.resize(
            (max(1, int(w * factor)), max(1, int(h * factor))), Image.Resampling.LANCZOS)

    def set_opacity(self, alpha: float):
        """alpha 0.0–1.0"""
        alpha = max(0.0, min(1.0, alpha))
        r, g, b, a = self.working_image.split()
        a = a.point(lambda p: int(p * alpha))
        self.working_image = Image.merge('RGBA', (r, g, b, a))

    def adjust_image(self, brightness: float = 1.0, contrast: float = 1.0, saturation: float = 1.0):
        """1.0 is original value"""
        if brightness != 1.0:
            self.working_image = ImageEnhance.Brightness(self.working_image).enhance(brightness)
        if contrast != 1.0:
            self.working_image = ImageEnhance.Contrast(self.working_image).enhance(contrast)
        if saturation != 1.0:
            self.working_image = ImageEnhance.Color(self.working_image).enhance(saturation)

    def flip_image(self, horizontal: bool = False, vertical: bool = False):
        if horizontal:
            self.working_image = self.working_image.transpose(Image.FLIP_LEFT_RIGHT)
        if vertical:
            self.working_image = self.working_image.transpose(Image.FLIP_TOP_BOTTOM)

    def add_padding(self, percent: float = 10):
        """Add transparent padding around icon (percent of canvas size)"""
        w, h = self.working_image.size
        pad = int(min(w, h) * percent / 100)
        new_w, new_h = w + pad * 2, h + pad * 2
        canvas = Image.new('RGBA', (new_w, new_h), (0, 0, 0, 0))
        canvas.paste(self.working_image, (pad, pad), self.working_image)
        self.working_image = canvas

    def add_background(self, color: tuple):
        """Add a solid or gradient background"""
        bg = Image.new('RGBA', self.working_image.size, color)
        bg.paste(self.working_image, (0, 0), self.working_image)
        self.working_image = bg

    def apply_circle_mask(self):
        """Clip the icon to a circle (like iOS app icons)"""
        w, h = self.working_image.size
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, w, h), fill=255)

        # Apply mask to alpha channel
        if self.working_image.mode != 'RGBA':
            self.working_image = self.working_image.convert('RGBA')

        r, g, b, a = self.working_image.split()
        new_a = ImageOps.fit(mask, a.size, centering=(0.5, 0.5))
        final_a = ImageChops.darker(a, new_a)
        self.working_image.putalpha(final_a)

    def apply_squircle_mask(self):
        """Clip to a superellipse / squircle (modern iOS style)"""
        w, h = self.working_image.size
        mask = Image.new('L', (1024, 1024), 0)
        draw = ImageDraw.Draw(mask)

        # Use rounded rectangle with max radius as approximation for squircle
        # For a true squircle we'd need a mathematical path
        radius = 260 # approx for 1024
        draw.rounded_rectangle((0, 0, 1024, 1024), radius=radius, fill=255)

        mask = mask.resize((w, h), Image.Resampling.LANCZOS)

        if self.working_image.mode != 'RGBA':
            self.working_image = self.working_image.convert('RGBA')

        r, g, b, a = self.working_image.split()
        final_a = ImageChops.darker(a, mask)
        self.working_image.putalpha(final_a)

    def apply_rounded_corners(self, radius_pct: float = 20):
        """Round the icon corners by a % of width"""
        w, h = self.working_image.size
        radius = int(min(w, h) * radius_pct / 100)
        mask = Image.new('L', (w, h), 0)
        draw = ImageDraw.Draw(mask)
        draw.rounded_rectangle((0, 0, w, h), radius=radius, fill=255)

        if self.working_image.mode != 'RGBA':
            self.working_image = self.working_image.convert('RGBA')

        r, g, b, a = self.working_image.split()
        final_a = ImageChops.darker(a, mask)
        self.working_image.putalpha(final_a)

    def add_border(self, width_pct: float = 3, color: tuple = (255, 255, 255, 255)):
        """Draw a colored border around the icon"""
        w, h  = self.working_image.size
        bw    = max(1, int(min(w, h) * width_pct / 100))
        draw  = ImageDraw.Draw(self.working_image)
        draw.rectangle([(bw//2, bw//2), (w - bw//2, h - bw//2)],
                       outline=color, width=bw)

    def add_shadow(self):
        """Add a realistic drop shadow beneath the icon"""
        w, h    = self.working_image.size
        shadow  = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        s_draw  = ImageDraw.Draw(shadow)
        s_draw.rectangle((10, 10, w - 10, h - 10), fill=(0, 0, 0, 120))
        shadow  = shadow.filter(ImageFilter.GaussianBlur(12))
        result  = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        result.alpha_composite(shadow)
        result.alpha_composite(self.working_image)
        self.working_image = result

    # ─── Text Overlay ─────────────────────────────────────────
    @staticmethod
    def _is_arabic(text: str) -> bool:
        return bool(re.search(r'[\u0600-\u06FF]', text))

    def add_text_overlay(self, text: str, font_path: str = None,
                         font_size_pct: float = 15, color: tuple = (255, 255, 255),
                         position: str = "bottom",
                         outline: bool = True, style: str = "Normal",
                         offset_x: int = 0, offset_y: int = 0):
        """
        Add a text badge onto the icon.
        font_size_pct: font size as % of canvas width (dynamic sizing).
        position: 'top' | 'center' | 'bottom'
        style: 'Normal', 'Upward (صاعد)', 'Slanted (مائل)'
        offset_x, offset_y: custom positioning
        """
        if not text: return
        img = self.working_image
        w, h = img.size
        fs   = max(12, int(w * font_size_pct / 100))

        # Extended layer for transformations
        ext_w, ext_h = w * 2, h * 2
        layer = Image.new("RGBA", (ext_w, ext_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        # Load font
        font = self._load_font(font_path, fs)

        dir_kw = {}
        if self._is_arabic(text):
            dir_kw = {"direction": "rtl", "language": "ar"}

        # Measure text using textbbox
        bbox = draw.textbbox((0, 0), text, font=font, **dir_kw)
        tw   = bbox[2] - bbox[0]
        th   = bbox[3] - bbox[1]

        # Position on extended layer
        x = (ext_w - tw) // 2 + offset_x
        if position == "top":
            y = (ext_h - h) // 2 + int(h * 0.05) + offset_y
        elif position == "center":
            y = (ext_h - th) // 2 + offset_y
        else:  # bottom
            y = (ext_h - h) // 2 + int(h * 0.82) - th + offset_y

        if outline:
            for dx, dy in [(-2, -2), (2, -2), (-2, 2), (2, 2), (0, -2), (0, 2), (-2, 0), (2, 0)]:
                draw.text((x + dx, y + dy), text, font=font, fill=(0, 0, 0, 180), **dir_kw)

        draw.text((x, y), text, font=font, fill=tuple(list(color)[:3] + [255]), **dir_kw)

        # Apply styles (transformations)
        if style == "Upward (صاعد)":
            layer = layer.rotate(10, Image.Resampling.BICUBIC, expand=False, center=(ext_w//2, ext_h//2))
        elif style == "Slanted (مائل)":
            layer = layer.transform(layer.size, Image.AFFINE, (1, -0.2, 0, 0, 1, 0), Image.Resampling.BICUBIC)

        px, py = (ext_w - w) // 2, (ext_h - h) // 2
        cropped_layer = layer.crop((px, py, px + w, py + h))
        img = Image.alpha_composite(img.convert("RGBA"), cropped_layer)
        self.working_image = img

    # ─── Helpers ──────────────────────────────────────────────
    @staticmethod
    def _load_font(path: str, size: int) -> ImageFont.FreeTypeFont:
        if path and os.path.exists(path):
            try: return ImageFont.truetype(path, size)
            except: pass
        paths = ["arialbd.ttf", "arial.ttf", "msgothic.ttc"]
        for p in paths:
            try: return ImageFont.truetype(p, size)
            except: pass
        return ImageFont.load_default()

    # ─── Export ───────────────────────────────────────────────
    def convert_to_ico(self, output_path: str, sizes: list | None = None, quality: int = 95):
        """
        Export ICO with largest-first frame order for maximum viewer compatibility.
        Supports up to 4096×4096.
        """
        if not self.working_image:
            raise Exception("No image loaded.")

        if sizes is None:
            # Default: all standard sizes up to 256 (safe ICO)
            sizes = [(16,16),(32,32),(48,48),(64,64),(128,128),(256,256)]

        # De-duplicate, sort descending (largest first)
        unique = sorted(set(sizes), key=lambda s: s[0], reverse=True)

        # NOTE: Pillow's ICO encoder internally caps at 256 per the ICO spec.
        # For sizes > 256 we save them as separate high-resolution PNGs alongside the ICO.
        ico_sizes  = [s for s in unique if s[0] <= 256]
        large_sizes = [s for s in unique if s[0] > 256]

        if ico_sizes:
            # Upscale working image to largest ICO frame first
            max_s = ico_sizes[0]
            save_base = self.working_image.copy().resize(max_s, Image.Resampling.LANCZOS)
            save_base.save(output_path, format="ICO", sizes=ico_sizes, quality=quality)

        # Save large "retina" PNGs next to the ICO
        large_paths = []
        if large_sizes:
            stem = Path(output_path).stem
            folder = Path(output_path).parent / f"{stem}_hires"
            folder.mkdir(parents=True, exist_ok=True)
            for s in large_sizes:
                resized = self.working_image.copy().resize(s, Image.Resampling.LANCZOS)
                p = folder / f"icon_{s[0]}x{s[1]}.png"
                resized.save(str(p), format="PNG", optimize=True)
                large_paths.append(str(p))

        return output_path, large_paths

    def export_all_sizes(self, output_folder: str):
        """Export every standard size as a separate PNG."""
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        results = []
        for s in self.STANDARD_SIZES:
            resized = self.working_image.copy().resize(s, Image.Resampling.LANCZOS)
            p = os.path.join(output_folder, f"icon_{s[0]}x{s[1]}.png")
            resized.save(p, 'PNG', optimize=True)
            results.append(p)
        return results

    def convert_to_webp(self, output_path: str, quality: int = 80, lossless: bool = False):
        if not self.working_image: raise Exception("No image loaded.")
        self.working_image.save(output_path, format="WEBP", quality=quality, lossless=lossless)
        return output_path

    def convert_to_pdf(self, output_path: str):
        if not self.working_image: raise Exception("No image loaded.")
        # PDF needs RGB (if transparent, we composite on white or keep RGBA if supported by some viewers,
        # but standard PIL PDF save prefers RGB)
        pdf_img = self.working_image.convert("RGB")
        pdf_img.save(output_path, format="PDF", resolution=100.0)
        return output_path
