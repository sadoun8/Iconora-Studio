"""
Iconora Studio - Signature Engine v2.0
"""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from pathlib import Path
import os

import re

DECORATIVE_FONTS = {
    "Brush Script MT":    "BRUSHSCI.TTF",
    "Edwardian Script":   "ITCEDSCR.TTF",
    "French Script MT":   "FRSCRIPT.TTF",
    "Vivaldi":            "VIVALDII.TTF",
    "Mistral":            "MISTRAL.TTF",
    "Lucida Handwriting": "LHANDW.TTF",
    "Segoe Script":       "segoesc.ttf",
    "Segoe Print":        "segoepr.ttf",
    "Comic Sans Bold":    "comicbd.ttf",
    "Gabriola":           "Gabriola.ttf",
    "Arial Bold":         "arialbd.ttf",
    "Calibri Bold":       "calibrib.ttf",
    "Segoe UI Bold":      "segoeuib.ttf",
}

CUSTOM_FONTS = {
    "Aref Ruqaa (عربي)": "ArefRuqaa-Regular.ttf",
    "Amiri (عربي)": "amiri-regular.ttf",
    "Cairo (عربي)": "Cairo.ttf",
    "Lemonada (عربي)": "Lemonada.ttf",
    "Katibeh (عربي)": "Katibeh.ttf",
    "Lateef (عربي)": "Lateef.ttf",
    "Reem Kufi (عربي)": "ReemKufi.ttf",
    "Great Vibes": "GreatVibes-Regular.ttf",
    "Pacifico": "Pacifico-Regular.ttf",
    "Dancing Script": "DancingScript.ttf",
    "Alex Brush": "AlexBrush.ttf",
    "Sacramento": "Sacramento.ttf",
}

ORNAMENTS = {
    "None":      "",
    "Flourish":  "\u2766",
    "Star Line": "\u2726\u2501\u2501\u2501\u2726",
    "Diamond":   "\u25c6 \u25c6 \u25c6",
    "Dots":      "\u00b7  \u00b7  \u00b7",
    "Em Dash":   "\u2014",
    "Asterism":  "\u2042",
    "Artistic Slash": "slash",
    "Artistic Undercurve": "undercurve",
    "Artistic Swirl": "swirl",
    "Artistic Double Strike": "double_strike",
    "Artistic Curve Up": "curve_up",
    "Artistic Loop Under": "loop_under",
    "Artistic Bracket Left": "bracket_left",
    "Artistic Bracket Right": "bracket_right",
}

WIN_FONTS = "C:\\Windows\\Fonts"


class SignatureEngine:
    def __init__(self, width=900, height=350):
        self.width = width
        self.height = height

    @staticmethod
    def available_fonts():
        found = {}
        assets_fonts = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'assets', 'fonts')

        # 1. Custom defined fonts (prioritized)
        for name, fn in CUSTOM_FONTS.items():
            p = os.path.join(assets_fonts, fn)
            if os.path.exists(p):
                found[name] = p

        # 2. Dynamic loading of all other fonts in assets/fonts
        if os.path.exists(assets_fonts):
            for file in os.listdir(assets_fonts):
                if file.lower().endswith(('.ttf', '.otf')):
                    # Check if already added via CUSTOM_FONTS
                    is_custom = False
                    for _, cf_fn in CUSTOM_FONTS.items():
                        if cf_fn.lower() == file.lower():
                            is_custom = True
                            break
                    
                    if not is_custom:
                        name = os.path.splitext(file)[0].replace("-", " ").title()
                        found[name] = os.path.join(assets_fonts, file)

        # 3. Decorative Windows system fonts
        for name, fn in DECORATIVE_FONTS.items():
            p = os.path.join(WIN_FONTS, fn)
            if os.path.exists(p):
                found[name] = p
        
        if not found:
            found["Arial Bold"] = None
        return found

    @staticmethod
    def ornament_names():
        return list(ORNAMENTS.keys())

    @staticmethod
    def _load_font(path, size):
        candidates = [
            path,
            os.path.join(WIN_FONTS, "arialbd.ttf"),
            os.path.join(WIN_FONTS, "arial.ttf"),
        ]
        for c in candidates:
            if c:
                try:
                    return ImageFont.truetype(c, size)
                except Exception:
                    pass
        return ImageFont.load_default()

    @staticmethod
    def _is_arabic(text):
        if not text: return False
        return bool(re.search(r'[\u0600-\u06FF]', text))

    def generate(self, name, title="", ornament="None",
                 font_path=None, title_font_path=None, font_size=90,
                 color=(20, 20, 80), title_color=None, opacity=1.0,
                 transparent=True, ink_effect=True, style="Normal",
                 bg_color=(255, 255, 255), spacing=15,
                 slant=0.0, thickness=1.0, rotation=0,
                 offset_x=0, offset_y=0):
        bg_a = 0 if transparent else 255
        canvas = Image.new("RGBA", (self.width, self.height),
                           (*bg_color[:3], bg_a))

        ext_w, ext_h = self.width * 2, self.height * 2
        layer = Image.new("RGBA", (ext_w, ext_h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(layer)

        mf = self._load_font(font_path, font_size)
        tf = self._load_font(title_font_path if title_font_path else font_path, max(18, font_size // 3))
        of = self._load_font(font_path, max(16, font_size // 4)) # Use the main font as fallback for ornaments
        try:
            of_sym = self._load_font(os.path.join(WIN_FONTS, "seguiemj.ttf"), max(16, font_size // 4))
            if of_sym.getname()[0] == "Segoe UI Emoji": of = of_sym
            else:
                of_sym = self._load_font(os.path.join(WIN_FONTS, "seguisym.ttf"), max(16, font_size // 4))
                if of_sym.getname()[0] == "Segoe UI Symbol": of = of_sym
        except:
            pass

        tc = title_color if title_color is not None else color
        lines = [("main", name, mf, color)]
        if title:
            lines.append(("title", title, tf, tc))
        
        # Check if it's a font-based or a stroke-based ornament
        orn_raw = ORNAMENTS.get(ornament, "")
        is_stroke_orn = orn_raw in ["slash", "undercurve", "swirl", "double_strike", "curve_up", "loop_under", "bracket_left", "bracket_right"]
        
        if orn_raw and not is_stroke_orn:
            lines.append(("orn", orn_raw, of, color))

        # Measure total height
        total_h = 0
        measured = []
        for kind, text, font, tcolor in lines:
            dir_kw = {"direction": "rtl", "language": "ar"} if self._is_arabic(text) else {}
            bb = draw.textbbox((0, 0), text, font=font, **dir_kw)
            tw = bb[2] - bb[0]
            th = bb[3] - bb[1]
            ty = bb[1]
            measured.append((kind, text, font, tcolor, tw, th, dir_kw, ty))
            total_h += th + spacing

        cy = (ext_h - total_h) // 2 + offset_y
        main_bbox = None
        
        for kind, text, font, tcolor, tw, th, dir_kw, ty in measured:
            cx = (ext_w - tw) // 2 + offset_x
            
            if kind == "main":
                main_bbox = (cx, cy, tw, th, ty)

            # Apply dynamic "Pressure Sensitive / Ink" Effect
            if ink_effect and kind == "main":
                # Create a subtle bleed mask (simulating ink spreading into paper)
                sh = Image.new("RGBA", layer.size, (0, 0, 0, 0))
                sd = ImageDraw.Draw(sh)

                # Base ink drop with thickness influence
                spread = 1.2 * thickness
                sd.text((cx, cy - ty), text, font=font, fill=(*tcolor[:3], 150), **dir_kw)

                # Pressure variation points
                sd.text((cx + 1, cy - ty + 1), text, font=font, fill=(*tcolor[:3], 100), **dir_kw)
                sd.text((cx - 1, cy - ty + 1), text, font=font, fill=(*tcolor[:3], 120), **dir_kw)

                # Blur to simulate ink spread
                sh = sh.filter(ImageFilter.GaussianBlur(spread))
                layer.alpha_composite(sh)

                # Deep core pressure (middle of the stroke)
                core = Image.new("RGBA", layer.size, (0, 0, 0, 0))
                cd = ImageDraw.Draw(core)
                cd.text((cx, cy - ty), text, font=font, fill=(*tcolor[:3], 240), **dir_kw)
                cd.text((cx + 1, cy - ty), text, font=font, fill=(*tcolor[:3], 200), **dir_kw) # Slight right drag
                layer.alpha_composite(core)

            else:
                base_alpha = 255 if kind == "main" else 200
                final_alpha = int(base_alpha * max(0.0, min(1.0, opacity)))
                draw.text((cx, cy - ty), text, font=font,
                          fill=(*tcolor[:3], final_alpha), **dir_kw)

            cy += th + spacing

        # Draw stroke-based ornaments
        if is_stroke_orn and main_bbox:
            cx, cy, tw, th, ty = main_bbox
            final_alpha = int(255 * max(0.0, min(1.0, opacity)))
            stroke_color = (*color[:3], final_alpha)
            stroke_w = max(2, int(font_size / 20 * thickness))
            
            # Re-check stroke_orn names since we added more
            if orn_raw == "slash":
                # A diagonal artistic slash behind/through the name
                draw.line([(cx - 20, cy + th + 10), (cx + tw + 40, cy - 20)], fill=stroke_color, width=stroke_w)
            elif orn_raw == "undercurve":
                # An elegant curved underline
                draw.arc([cx - 30, cy + th - 10, cx + tw + 30, cy + th + 40], start=0, end=180, fill=stroke_color, width=stroke_w)
            elif orn_raw == "swirl":
                # A circular swirl at the beginning
                swirl_r = int(th * 0.8)
                draw.arc([cx - swirl_r, cy - 10, cx + 10, cy + th + 10], start=45, end=330, fill=stroke_color, width=stroke_w)
            elif orn_raw == "double_strike":
                # Two horizontal artistic strokes
                draw.line([(cx - 10, cy + th + 5), (cx + tw + 10, cy + th + 5)], fill=stroke_color, width=stroke_w)
                draw.line([(cx - 5, cy + th + 12), (cx + tw + 15, cy + th + 12)], fill=stroke_color, width=stroke_w)
            elif orn_raw == "curve_up":
                # A curve above the name
                draw.arc([cx - 20, cy - 40, cx + tw + 20, cy + 10], start=180, end=0, fill=stroke_color, width=stroke_w)
            elif orn_raw == "loop_under":
                # A stylish loop under the name
                draw.arc([cx + tw//4, cy + th, cx + tw*3//4, cy + th + 30], start=0, end=360, fill=stroke_color, width=stroke_w)
                draw.line([(cx, cy + th + 10), (cx + tw, cy + th + 10)], fill=stroke_color, width=stroke_w)
            elif orn_raw == "bracket_left":
                draw.arc([cx - 40, cy - 20, cx - 10, cy + th + 20], start=90, end=270, fill=stroke_color, width=stroke_w)
            elif orn_raw == "bracket_right":
                draw.arc([cx + tw + 10, cy - 20, cx + tw + 40, cy + th + 20], start=270, end=90, fill=stroke_color, width=stroke_w)

        # Apply styles (transformations)
        if slant != 0:
            layer = layer.transform(layer.size, Image.AFFINE, (1, -slant, 0, 0, 1, 0), Image.Resampling.BICUBIC)
        
        if rotation != 0:
            layer = layer.rotate(rotation, Image.Resampling.BICUBIC, expand=False, center=(ext_w//2, ext_h//2))
        elif style == "Upward (صاعد)":
            layer = layer.rotate(10, Image.Resampling.BICUBIC, expand=False, center=(ext_w//2, ext_h//2))
        elif style == "Slanted (مائل)":
            # Affine matrix for horizontal shearing
            layer = layer.transform(layer.size, Image.AFFINE, (1, -0.2, 0, 0, 1, 0), Image.Resampling.BICUBIC)

        # Composite transformed layer onto main canvas
        px, py = (ext_w - self.width) // 2, (ext_h - self.height) // 2
        canvas.alpha_composite(layer.crop((px, py, px + self.width, py + self.height)))

        return canvas

    def save(self, image, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        ext = Path(path).suffix.lower()
        
        if ext == ".pdf":
            # PDF doesn't support transparency well in all viewers, so we flatten to white if needed
            # but usually for logos, we just save the RGB version
            pdf_img = image.convert("RGB")
            pdf_img.save(path, "PDF", resolution=300.0)
        elif ext == ".webp":
            image.save(path, "WEBP", quality=90, lossless=True)
        else:
            image.save(path, "PNG", optimize=True)
        return path

    # --- Legacy compatibility ---
    def generate_signature(self, text, font_path=None, font_size=60,
                           color=(0, 0, 0), ink_effect=True,
                           background_color=(255, 255, 255)):
        return self.generate(name=text, font_path=font_path,
                             font_size=font_size, color=color,
                             ink_effect=ink_effect, transparent=False,
                             bg_color=background_color)

    def save_signature(self, image, path):
        return self.save(image, path)
