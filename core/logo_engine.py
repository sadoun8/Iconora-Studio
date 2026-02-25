"""
Logo Design Engine
محرك تصميم الشعارات

Professional logo generation with support for custom fonts, colors, and gradients
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from pathlib import Path
from i18n import tr


class GradientGenerator:
    """توليد التدرجات اللونية / Generate color gradients"""

    @staticmethod
    def linear_gradient(width, height, color1, color2, direction="horizontal"):
        """
        إنشاء تدرج خطي / Create linear gradient

        Args:
            width: عرض الصورة / Image width
            height: ارتفاع الصورة / Image height
            color1: اللون الأول / Color 1 (RGBA tuple or hex)
            color2: اللون الثاني / Color 2 (RGBA tuple or hex)
            direction: الاتجاه (horizontal/vertical/diagonal)

        Returns:
            Image: صورة التدرج / Gradient image
        """
        def to_rgba(c):
            if isinstance(c, tuple):
                return c
            c = c.lstrip("#")
            return tuple(int(c[i:i+2], 16) for i in (0, 2, 4)) + (255,)

        c1 = to_rgba(color1)
        c2 = to_rgba(color2)

        image = Image.new("RGBA", (width, height), c1)
        draw = ImageDraw.Draw(image)

        if direction == "horizontal":
            for x in range(width):
                ratio = x / max(1, width - 1)
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                a = int(c1[3] * (1 - ratio) + c2[3] * ratio)
                draw.line([(x, 0), (x, height)], fill=(r, g, b, a))

        elif direction == "vertical":
            for y in range(height):
                ratio = y / max(1, height - 1)
                r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                a = int(c1[3] * (1 - ratio) + c2[3] * ratio)
                draw.line([(0, y), (width, y)], fill=(r, g, b, a))

        else:  # diagonal
            for x in range(width):
                for y in range(height):
                    ratio = (x + y) / max(1, (width + height - 2))
                    r = int(c1[0] * (1 - ratio) + c2[0] * ratio)
                    g = int(c1[1] * (1 - ratio) + c2[1] * ratio)
                    b = int(c1[2] * (1 - ratio) + c2[2] * ratio)
                    a = int(c1[3] * (1 - ratio) + c2[3] * ratio)
                    image.putpixel((x, y), (r, g, b, a))

        return image

    @staticmethod
    def hex_to_rgba(hex_color, alpha=255):
        """Convert hex color to RGBA"""
        hex_color = hex_color.lstrip("#")
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)
        return (255, 255, 255, alpha)


class LogoEngine:
    """محرك تصميم الشعارات / Logo Design Engine"""

    def __init__(self, export_folder="exports/logos"):
        self.export_folder = export_folder
        self.width = 900
        self.height = 450
        Path(export_folder).mkdir(parents=True, exist_ok=True)

    def create_gradient(self, size, color1, color2, vertical=True):
        w, h = size
        direction = "vertical" if vertical else "horizontal"
        return GradientGenerator.linear_gradient(w, h, color1, color2, direction)

    def generate_logo(self, text, font_path, font_size,
                      style="Minimal",
                      color1="#ffffff",
                      color2="#ffffff",
                      shadow=True):
        """Generate a logo and return output path (string)."""
        width, height = self.width, self.height
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        # load font
        try:
            font = ImageFont.truetype(font_path, font_size) if font_path else ImageFont.load_default()
        except Exception:
            font = ImageFont.load_default()

        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]

        x = (width - text_w) // 2
        y = (height - text_h) // 2

        # prepare gradient/fill
        if style == "Luxury":
            grad = self.create_gradient((text_w, text_h), "#d4af37", "#8b7a33", vertical=False)
        elif style == "3D":
            grad = self.create_gradient((text_w, text_h), color1, color2, vertical=True)
        else:
            grad = Image.new("RGBA", (text_w, text_h), color1)

        # text mask
        text_mask = Image.new("L", (text_w, text_h), 0)
        md = ImageDraw.Draw(text_mask)
        md.text((0, 0), text, font=font, fill=255)

        # shadow
        if shadow:
            shadow_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            sd = ImageDraw.Draw(shadow_layer)
            sd.text((x + 6, y + 6), text, font=font, fill=(0, 0, 0, 200))
            shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(6))
            image = Image.alpha_composite(image, shadow_layer)

        # paste gradient
        image.paste(grad, (x, y), text_mask)

        # small emboss for 3D
        if style == "3D":
            edge = image.filter(ImageFilter.UnsharpMask(radius=2, percent=120, threshold=3))
            image = Image.alpha_composite(edge, image)

        safe_text = "_".join(text.split()) or "logo"
        output_path = os.path.join(self.export_folder, f"{safe_text}_logo.png")
        # avoid overwrite
        counter = 1
        base = output_path
        while os.path.exists(output_path):
            name, ext = os.path.splitext(base)
            output_path = f"{name}_{counter}{ext}"
            counter += 1

        image.save(output_path)
        return output_path

    def get_system_fonts(self):
        fonts = {}
        try:
            fonts_dir = "C:\\Windows\\Fonts"
            if os.path.exists(fonts_dir):
                for font_file in os.listdir(fonts_dir):
                    if font_file.lower().endswith(('.ttf', '.otf')):
                        name = os.path.splitext(font_file)[0]
                        fonts[name] = os.path.join(fonts_dir, font_file)
        except Exception:
            pass
        return fonts

    def batch_generate_logos(self, logos_data):
        results = {"success": [], "failed": [], "total": len(logos_data)}
        for info in logos_data:
            try:
                out = self.generate_logo(**info)
                results["success"].append({"text": info.get("text"), "path": out})
            except Exception as e:
                results["failed"].append({"text": info.get("text"), "error": str(e)})
        return results

    def resize_logo(self, logo_path, width, height):
        try:
            img = Image.open(logo_path)
            img = img.resize((width, height), Image.Resampling.LANCZOS)
            name, ext = os.path.splitext(logo_path)
            new_path = f"{name}_{width}x{height}{ext}"
            img.save(new_path)
            return new_path
        except Exception as e:
            raise Exception(f"{tr('msg_error_occurred')}{str(e)}")

    def apply_watermark(self, logo_path, watermark_text, watermark_opacity=100):
        try:
            img = Image.open(logo_path).convert("RGBA")
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            watermark_color = (200, 200, 200, watermark_opacity)
            draw.text((10, img.height - 30), watermark_text, font=font, fill=watermark_color)
            name, ext = os.path.splitext(logo_path)
            new_path = f"{name}_watermarked{ext}"
            img.save(new_path)
            return new_path
        except Exception as e:
            raise Exception(f"{tr('msg_error_occurred')}{str(e)}")
