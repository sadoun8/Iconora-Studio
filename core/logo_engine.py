"""Iconora Studio - Logo Engine v2.0"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageChops

try:
    from rembg import remove
    HAS_REMBG = True
except ImportError:
    remove = None
    HAS_REMBG = False

from pathlib import Path
import os
import re

WIN_FONTS = "C:\\Windows\\Fonts"

FONT_CATALOG = {
    "Arial Bold":    "arialbd.ttf",
    "Arial":         "arial.ttf",
    "Times Bold":    "timesbd.ttf",
    "Verdana Bold":  "verdanab.ttf",
    "Georgia Bold":  "georgiab.ttf",
    "Trebuchet MS":  "trebucbd.ttf",
    "Comic Sans":    "comicbd.ttf",
    "Calibri Bold":  "calibrib.ttf",
    "Segoe UI Bold": "segoeuib.ttf",
    "Impact":        "impact.ttf",
    "Tahoma Bold":   "tahomabd.ttf",
}

TEMPLATES = {
    "Modern Clean": {
        "bg": (15, 23, 42, 255), "text_color1": (255, 255, 255),
        "accent": (99, 102, 241), "shape": "none",
    },
    "Corporate Blue": {
        "bg": (30, 64, 175, 255), "text_color1": (255, 255, 255),
        "accent": (147, 197, 253), "shape": "bar",
    },
    "Startup Gradient": {
        "bg": "gradient_purple", "text_color1": (255, 255, 255),
        "accent": (236, 72, 153), "shape": "none",
    },
    "Elegant Gold": {
        "bg": (17, 17, 17, 255), "text_color1": (212, 175, 55),
        "accent": (180, 140, 30), "shape": "underline",
    },
    "Nature Green": {
        "bg": (20, 83, 45, 255), "text_color1": (255, 255, 255),
        "accent": (134, 239, 172), "shape": "circle",
    },
    "Vibrant Orange": {
        "bg": (234, 88, 12, 255), "text_color1": (255, 255, 255),
        "accent": (251, 191, 36), "shape": "none",
    },
    "White Minimal": {
        "bg": (255, 255, 255, 255), "text_color1": (15, 23, 42),
        "accent": (99, 102, 241), "shape": "dot",
    },
    "Neon Dark": {
        "bg": (0, 0, 0, 255), "text_color1": (0, 255, 200),
        "accent": (180, 0, 255), "shape": "none",
    },
    "Square Framed": {
        "bg": (20, 20, 20, 255), "text_color1": (255, 255, 255),
        "accent": (239, 68, 68), "shape": "square",
    },
    "Polygon Art": {
        "bg": (243, 244, 246, 255), "text_color1": (31, 41, 55),
        "accent": (16, 185, 129), "shape": "polygon",
    },
    "Luxury Gold & Black": {
        "bg": (10, 10, 10, 255), "text_color1": (255, 215, 0),
        "accent": (218, 165, 32), "shape": "polygon"
    },
    "Emerald Royal": {
        "bg": (4, 47, 46, 255), "text_color1": (167, 243, 208),
        "accent": (5, 150, 105), "shape": "square"
    },
    "Midnight Violet": {
        "bg": "gradient_midnight", "text_color1": (216, 180, 254),
        "accent": (168, 85, 247), "shape": "dot"
    },
    "Premium Gold": {
        "bg": (10, 10, 10, 255), "text_color1": (255, 215, 0, 255),
        "accent": (218, 165, 32, 255), "shape": "polygon"
    },
    "Cyber Neon": {
        "bg": (0, 0, 0, 255), "text_color1": (0, 255, 255, 255),
        "accent": (255, 0, 255, 255), "shape": "circle"
    },
    "Eco Bio": {
        "bg": (240, 253, 244, 255), "text_color1": (22, 101, 52, 255),
        "accent": (34, 197, 94, 255), "shape": "none"
    }
}

class LogoEngine:
    STYLES = ["Minimal", "Luxury", "3D", "Outlined", "Retro", "Neon Glow", "Modern Shadow", "Glassy", "Gradient"]

    def __init__(self, width=900, height=450):
        self.width = width
        self.height = height
        self.icon = None

    def load_icon(self, path):
        try:
            img = Image.open(path)
            if img.mode != "RGBA":
                img = img.convert("RGBA")
            self.icon = img
            return True
        except Exception as e:
            print(f"load_icon error: {e}")
            return False

    def remove_icon_bg(self):
        """Remove background from loaded icon using AI (rembg)"""
        if not HAS_REMBG:
            raise ImportError("rembg is not installed. Install with `pip install rembg` to enable background removal.")
        if self.icon:
            self.icon = remove(self.icon)
            return True
        return False

    def clear_icon(self):
        self.icon = None

    @staticmethod
    def available_fonts():
        from core.signature_engine import SignatureEngine
        return SignatureEngine(200, 200).available_fonts()

    @staticmethod
    def template_names():
        return list(TEMPLATES.keys())

    @staticmethod
    def _load_font(path, size):
        candidates = [path, os.path.join(WIN_FONTS, "arialbd.ttf"),
                      os.path.join(WIN_FONTS, "arial.ttf")]
        for c in candidates:
            if c:
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    def _make_background(self, tmpl):
        spec = tmpl.get("bg", (30, 30, 30, 255))
        if spec == "gradient_purple":
            canvas = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(canvas)
            for x in range(self.width):
                r = int(88  + (236 - 88)  * x / self.width)
                g = int(28  + (72  - 28)  * x / self.width)
                b = int(135 + (153 - 135) * x / self.width)
                draw.line([(x, 0), (x, self.height)], fill=(r, g, b, 255))
        elif spec == "gradient_midnight":
            canvas = Image.new("RGBA", (self.width, self.height))
            draw = ImageDraw.Draw(canvas)
            for x in range(self.width):
                r = int(15  + (40 - 15)  * x / self.width)
                g = int(23  + (30 - 23)  * x / self.width)
                b = int(42  + (80 - 42)  * x / self.width)
                draw.line([(x, 0), (x, self.height)], fill=(r, g, b, 255))
        else:
            canvas = Image.new("RGBA", (self.width, self.height), spec)
        return canvas

    def _draw_shape(self, canvas, tmpl, text_y, text_h, accent):
        draw = ImageDraw.Draw(canvas)
        shape = tmpl.get("shape", "none")
        if shape == "bar":
            draw.rectangle([(30, self.height - 12),
                             (self.width - 30, self.height - 7)], fill=accent)
        elif shape == "underline":
            y = text_y + text_h + 10
            draw.rectangle([(40, y), (self.width - 40, y + 4)], fill=accent)
        elif shape == "circle":
            r = min(self.width, self.height) * 0.44
            cx, cy = self.width // 2, self.height // 2
            draw.ellipse([(cx - r, cy - r), (cx + r, cy + r)],
                         outline=accent, width=3)
        elif shape == "dot":
            draw.ellipse([(self.width // 2 - 5, self.height - 26),
                          (self.width // 2 + 5, self.height - 16)], fill=accent)
        elif shape == "square":
            p = min(self.width, self.height) * 0.1
            draw.rectangle([(p, p), (self.width - p, self.height - p)], outline=accent, width=5)
        elif shape == "polygon":
            cx, cy = self.width // 2, self.height // 2
            r = min(self.width, self.height) * 0.45
            import math
            pts = []
            for i in range(6):
                angle = math.pi / 3 * i
                pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
            draw.polygon(pts, outline=accent, width=4)

    def generate_logo(self, text, style="Minimal",
                      color1=(99, 102, 241), color2=(255, 255, 255),
                      font_size=80, layout="side",
                      font_path=None, template_name=None,
                      icon_size_factor=1.0,
                      icon_rotation=0, icon_opacity=1.0, icon_saturation=1.0,
                      text_overlay=False, canvas_size=(800, 800),
                      text_offset_x=0, text_offset_y=0,
                      icon_offset_x=0, icon_offset_y=0,
                      shadow_color=(0, 0, 0), shadow_opacity=100,
                      shadow_blur=5, shadow_offset=(4, 4),
                      glow_color=None, glow_radius=10):
        """
        layout: "side" | "top" | "bottom"
        icon_size_factor: 0.1 - 3.0, scales icon relative to font_size
        text_overlay: when True, text is drawn ON TOP of the icon (full canvas)
        """
        self.width, self.height = canvas_size
        tmpl = TEMPLATES.get(template_name, {}) if template_name else {}
        canvas = self._make_background(tmpl) if tmpl else Image.new(
            "RGBA", (self.width, self.height), (255, 255, 255, 0))

        fp = font_path or os.path.join(WIN_FONTS, "arialbd.ttf")
        font = self._load_font(fp, font_size)

        dir_kw = {}
        if bool(re.search(r'[\u0600-\u06FF]', text)):
            dir_kw = {"direction": "rtl", "language": "ar"}

        tmp_draw = ImageDraw.Draw(canvas)
        bb = tmp_draw.textbbox((0, 0), text, font=font, **dir_kw)
        tw, th = bb[2] - bb[0], bb[3] - bb[1]

        icon_frame = None
        iw = ih = 0

        if self.icon:
            # Scale icon
            ih = int(font_size * 1.6 * icon_size_factor)
            iw = int(ih * self.icon.width / self.icon.height)
            icon_frame = self.icon.resize((iw, ih), Image.Resampling.LANCZOS)

            # Rotation
            if icon_rotation != 0:
                icon_frame = icon_frame.rotate(icon_rotation, Image.Resampling.BICUBIC, expand=True)
                iw, ih = icon_frame.size

            # Saturation
            if icon_saturation != 1.0:
                enhancer = ImageEnhance.Color(icon_frame)
                icon_frame = enhancer.enhance(icon_saturation)

            # Opacity
            if icon_opacity < 1.0:
                alpha = icon_frame.getchannel('A')
                new_alpha = alpha.point(lambda p: int(p * icon_opacity))
                icon_frame.putalpha(new_alpha)

        text_color  = tmpl.get("text_color1", color1) if tmpl else color1
        text_color2 = tmpl.get("accent", color2)      if tmpl else color2

        gap = 24

        if text_overlay and icon_frame:
            # Fill canvas with icon (centered), then overlay text on top
            max_size = min(self.width, self.height) * min(3.0, icon_size_factor)
            bg_icon = icon_frame.copy()
            bg_icon.thumbnail((int(max_size), int(max_size)), Image.Resampling.LANCZOS)
            bx = (self.width - bg_icon.width) // 2 + icon_offset_x
            by = (self.height - bg_icon.height) // 2 + icon_offset_y
            canvas.paste(bg_icon, (bx, by), bg_icon)

            text_x = (self.width - tw) // 2
            text_y = (self.height - th) // 2
            text_x += text_offset_x
            text_y += text_offset_y
            self._draw_styled_text(canvas, text, text_x, text_y, font,
                                   style, text_color, text_color2, dir_kw,
                                   (*shadow_color, shadow_opacity), shadow_blur, shadow_offset,
                                   glow_color, glow_radius)

        elif layout == "side":
            total_w = (iw + gap if icon_frame else 0) + tw
            sx = (self.width - total_w) // 2
            
            is_rtl = dir_kw.get("direction") == "rtl"
            
            if icon_frame:
                if is_rtl:
                    # Icon on the right, text on the left
                    text_x = sx + text_offset_x
                    ix = sx + tw + gap + icon_offset_x
                else:
                    # Icon on the left, text on the right
                    ix = sx + icon_offset_x
                    text_x = sx + iw + gap + text_offset_x
                
                iy = (self.height - ih) // 2 + icon_offset_y
                canvas.paste(icon_frame, (ix, iy), icon_frame)
            else:
                text_x = (self.width - tw) // 2 + text_offset_x
            
            text_y = (self.height - th) // 2 + text_offset_y
            self._draw_styled_text(canvas, text, text_x, text_y, font,
                                   style, text_color, text_color2, dir_kw,
                                   (*shadow_color, shadow_opacity), shadow_blur, shadow_offset,
                                   glow_color, glow_radius)

        elif layout == "top":
            total_h = (ih + gap if icon_frame else 0) + th
            sy = (self.height - total_h) // 2
            if icon_frame:
                ix = (self.width - iw) // 2 + icon_offset_x
                iy = sy + icon_offset_y
                canvas.paste(icon_frame, (ix, iy), icon_frame)
                text_y = sy + ih + gap
            else:
                text_y = (self.height - th) // 2
            text_x = (self.width - tw) // 2
            text_x += text_offset_x
            text_y += text_offset_y
            self._draw_styled_text(canvas, text, text_x, text_y, font,
                                   style, text_color, text_color2, dir_kw,
                                   (*shadow_color, shadow_opacity), shadow_blur, shadow_offset,
                                   glow_color, glow_radius)

        else:  # bottom layout
            total_h = (ih + gap if icon_frame else 0) + th
            sy = (self.height - total_h) // 2
            text_y = sy
            if icon_frame:
                iy = sy + th + gap + icon_offset_y
                ix = (self.width - iw) // 2 + icon_offset_x
                canvas.paste(icon_frame, (ix, iy), icon_frame)
            text_x = (self.width - tw) // 2
            text_x += text_offset_x
            text_y += text_offset_y
            self._draw_styled_text(canvas, text, text_x, text_y, font,
                                   style, text_color, text_color2, dir_kw,
                                   (*shadow_color, shadow_opacity), shadow_blur, shadow_offset,
                                   glow_color, glow_radius)

        if tmpl:
            accent = tmpl.get("accent", (99, 102, 241))
            self._draw_shape(canvas, tmpl, text_y if "text_y" in locals() else 0, th, accent)

        return canvas

    def _draw_styled_text(self, canvas, text, x, y, font, style, c1, c2, dir_kw,
                          shadow_color, shadow_blur, shadow_offset,
                          glow_color, glow_radius):
        draw = ImageDraw.Draw(canvas)

        # Generic Shadow/Glow
        if shadow_blur > 0 or any(d != 0 for d in shadow_offset):
            sh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            sd = ImageDraw.Draw(sh)
            sd.text((x + shadow_offset[0], y + shadow_offset[1]), text, font=font, fill=shadow_color, **dir_kw)
            if shadow_blur > 0:
                sh = sh.filter(ImageFilter.GaussianBlur(shadow_blur))
            canvas.alpha_composite(sh)

        if glow_color and glow_radius > 0:
            gh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(gh)
            gd.text((x, y), text, font=font, fill=glow_color, **dir_kw)
            gh = gh.filter(ImageFilter.GaussianBlur(glow_radius))
            canvas.alpha_composite(gh)

        # Style-specific drawing
        if style == "Luxury":
            pass
        elif style == "3D":
            for i in range(7, 0, -1):
                alpha = int(200 * i / 7)
                draw.text((x + i, y + i), text, font=font,
                          fill=(*c2[:3], alpha), **dir_kw)
        elif style == "Outlined":
            for dx, dy in [(-2,-2),(2,-2),(-2,2),(2,2),(0,-3),(0,3),(-3,0),(3,0)]:
                draw.text((x+dx, y+dy), text, font=font, fill=(*c2[:3], 255), **dir_kw)
        elif style == "Retro":
            draw.text((x+3, y+3), text, font=font, fill=(*c2[:3], 200), **dir_kw)
        elif style == "Neon Glow":
            nsh = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            nsd = ImageDraw.Draw(nsh)
            nsd.text((x, y), text, font=font, fill=(*c2[:3], 255), **dir_kw)
            sh1 = nsh.filter(ImageFilter.GaussianBlur(15))
            sh2 = nsh.filter(ImageFilter.GaussianBlur(5))
            canvas.alpha_composite(sh1)
            canvas.alpha_composite(sh2)
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 255), **dir_kw)
            return
        elif style == "Modern Shadow":
            for i in range(1, 15):
                draw.text((x + i, y + i), text, font=font, fill=(0, 0, 0, int(30 * (1 - i/15))), **dir_kw)

        elif style == "Glassy":
            # Glassmorphism effect: Frosted glass behind text
            bb = draw.textbbox((x, y), text, font=font, **dir_kw)
            pad = 20
            glass_rect = [bb[0]-pad, bb[1]-pad, bb[2]+pad, bb[3]+pad]

            # Create glass layer
            glass = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            gd = ImageDraw.Draw(glass)
            gd.rounded_rectangle(glass_rect, radius=15, fill=(255, 255, 255, 40), outline=(255, 255, 255, 80), width=2)

            # Apply blur to the area UNDER the glass (simulated by blurring the glass itself if it had content,
            # but here we just overlay a semi-transparent white with border)
            canvas.alpha_composite(glass)
            draw.text((x, y), text, font=font, fill=(255, 255, 255, 200), **dir_kw)
            return

        elif style == "Gradient":
            # Simulation of linear gradient text (Top to Bottom)
            mask = Image.new("L", canvas.size, 0)
            md = ImageDraw.Draw(mask)
            md.text((x, y), text, font=font, fill=255, **dir_kw)

            bb = md.textbbox((x, y), text, font=font, **dir_kw)
            th = max(1, bb[3] - bb[1])

            grad_layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
            grd = ImageDraw.Draw(grad_layer)
            for i in range(bb[1], bb[3] + 1):
                ratio = (i - bb[1]) / th
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                grd.line([(bb[0], i), (bb[2], i)], fill=(r, g, b, 255))

            # Composite using text mask
            canvas.paste(grad_layer, (0, 0), mask)
            return

        draw.text((x, y), text, font=font, fill=(*c1[:3], 255), **dir_kw)

    def apply_watermark(self, base_image_path, logo_image, position="bottom-right", scale=0.2, opacity=0.7, padding=20):
        """Apply logo as watermark to another image"""
        try:
            base = Image.open(base_image_path)
            if base.mode != "RGBA":
                base = base.convert("RGBA")
            
            # Scale logo
            bw, bh = base.size
            lw, lh = logo_image.size
            
            # Max width based on scale
            max_lw = int(bw * scale)
            ratio = max_lw / lw
            target_lw = max_lw
            target_lh = int(lh * ratio)
            
            logo = logo_image.resize((target_lw, target_lh), Image.Resampling.LANCZOS)
            
            # Apply opacity
            if opacity < 1.0:
                alpha = logo.getchannel('A')
                new_alpha = alpha.point(lambda p: int(p * opacity))
                logo.putalpha(new_alpha)
            
            # Calculate position
            if position == "bottom-right":
                pos = (bw - target_lw - padding, bh - target_lh - padding)
            elif position == "bottom-left":
                pos = (padding, bh - target_lh - padding)
            elif position == "top-right":
                pos = (bw - target_lw - padding, padding)
            elif position == "top-left":
                pos = (padding, padding)
            elif position == "center":
                pos = ((bw - target_lw) // 2, (bh - target_lh) // 2)
            else:
                pos = (bw - target_lw - padding, bh - target_lh - padding)
                
            base.alpha_composite(logo, pos)
            return base
        except Exception as e:
            raise Exception(f"Watermarking failed: {e}")

    def save_logo(self, image, output_path):
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        ext = Path(output_path).suffix.lower()
        
        if ext == ".pdf":
            # PDF doesn't support transparency well in all viewers, so we flatten to white if needed
            # but usually for logos, we just save the RGB version
            pdf_img = image.convert("RGB")
            pdf_img.save(output_path, "PDF", resolution=300.0)
        elif ext == ".webp":
            image.save(output_path, "WEBP", quality=90, lossless=True)
        else:
            image.save(output_path, "PNG", optimize=True)
        return output_path
