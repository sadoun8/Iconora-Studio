"""
Signature Engine
محرك التوقيع الاحترافي

Professional signature generation with ink effects and customizable fonts.
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
from pathlib import Path


class SignatureEngine:
    """Professional signature generator with ink effects."""

    def __init__(self, export_folder="exports/signatures"):
        self.export_folder = export_folder
        Path(export_folder).mkdir(parents=True, exist_ok=True)

    def generate_signature(self, text, font_path, font_size=80, color="#000000",
                          ink_effect=True, width=800, height=250):
        """Generate a professional signature with optional ink effect.

        Args:
            text: Signature text (name)
            font_path: Path to TTF/OTF font file
            font_size: Font size in pixels
            color: Text color in hex (e.g., "#000000")
            ink_effect: Apply ink/shadow effect
            width: Canvas width
            height: Canvas height

        Returns:
            str: Path to generated signature PNG
        """
        try:
            # Load font
            try:
                font = ImageFont.truetype(font_path, font_size)
            except Exception:
                font = ImageFont.load_default()

            # Create transparent background
            image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            # Calculate text position (centered)
            bbox = draw.textbbox((0, 0), text, font=font)
            text_w = bbox[2] - bbox[0]
            text_h = bbox[3] - bbox[1]

            x = (width - text_w) // 2
            y = (height - text_h) // 2

            # Convert hex color to RGB tuple
            hex_color = color.lstrip("#")
            rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
            rgba_color = rgb_color + (255,)

            # Draw ink shadow (optional)
            if ink_effect:
                shadow_color = (0, 0, 0, 100)
                draw.text((x + 3, y + 3), text, font=font, fill=shadow_color)

            # Draw main text
            draw.text((x, y), text, font=font, fill=rgba_color)

            # Apply slight blur for ink effect
            if ink_effect:
                image = image.filter(ImageFilter.GaussianBlur(radius=0.8))

            # Save file
            safe_text = "_".join(text.split()) or "signature"
            output_path = os.path.join(self.export_folder, f"{safe_text}_signature.png")

            # Avoid overwrite
            counter = 1
            base = output_path
            while os.path.exists(output_path):
                name, ext = os.path.splitext(base)
                output_path = f"{name}_{counter}{ext}"
                counter += 1

            image.save(output_path)
            return output_path

        except Exception as e:
            raise Exception(f"Signature generation failed: {e}")

    def generate_signature_with_title(self, name, title, font_path, font_size=80,
                                     color="#000000", ink_effect=True):
        """Generate signature with name and title on separate lines.

        Args:
            name: Person's name
            title: Job title/position
            font_path: Font path
            font_size: Font size
            color: Text color
            ink_effect: Apply ink effect

        Returns:
            str: Path to generated signature
        """
        width, height = 800, 300
        image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)

        try:
            font = ImageFont.truetype(font_path, font_size)
            title_font = ImageFont.truetype(font_path, int(font_size * 0.6))
        except Exception:
            font = ImageFont.load_default()
            title_font = ImageFont.load_default()

        # Convert color
        hex_color = color.lstrip("#")
        rgb_color = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        rgba_color = rgb_color + (255,)

        # Calculate positions
        name_bbox = draw.textbbox((0, 0), name, font=font)
        name_w = name_bbox[2] - name_bbox[0]
        name_h = name_bbox[3] - name_bbox[1]

        title_bbox = draw.textbbox((0, 0), title, font=title_font)
        title_w = title_bbox[2] - title_bbox[0]
        title_h = title_bbox[3] - title_bbox[1]

        name_x = (width - name_w) // 2
        name_y = (height - name_h - title_h - 20) // 2

        title_x = (width - title_w) // 2
        title_y = name_y + name_h + 10

        # Draw shadow (optional)
        if ink_effect:
            shadow_color = (0, 0, 0, 100)
            draw.text((name_x + 2, name_y + 2), name, font=font, fill=shadow_color)
            draw.text((title_x + 2, title_y + 2), title, font=title_font, fill=shadow_color)

        # Draw main text
        draw.text((name_x, name_y), name, font=font, fill=rgba_color)
        draw.text((title_x, title_y), title, font=title_font, fill=rgba_color)

        # Apply blur
        if ink_effect:
            image = image.filter(ImageFilter.GaussianBlur(radius=0.8))

        # Save
        safe_name = "_".join(name.split()) or "signature"
        output_path = os.path.join(self.export_folder, f"{safe_name}_with_title.png")

        counter = 1
        base = output_path
        while os.path.exists(output_path):
            name_part, ext = os.path.splitext(base)
            output_path = f"{name_part}_{counter}{ext}"
            counter += 1

        image.save(output_path)
        return output_path
