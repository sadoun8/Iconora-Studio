"""
Palette Engine
محرك لوحات الألوان

Smart color palette generator with predefined luxury and modern sets.
"""

from PIL import Image, ImageDraw
import os
from pathlib import Path


class PaletteEngine:
    """Generate professional color palettes."""

    def __init__(self, export_folder="exports/palettes"):
        self.export_folder = export_folder
        Path(export_folder).mkdir(parents=True, exist_ok=True)

        # Predefined luxury palettes
        self.luxury_sets = [
            {
                "name": "Gold Elegance",
                "colors": ["#d4af37", "#000000", "#1a1a1a", "#e8dcc8", "#3d3d3d"]
            },
            {
                "name": "Silver Supreme",
                "colors": ["#c0c0c0", "#1e1e1e", "#2a2a2a", "#e5e5e5", "#404040"]
            },
            {
                "name": "Deep Blue Royalty",
                "colors": ["#0f2027", "#2c5364", "#203a43", "#1e3a5f", "#16213e"]
            }
        ]

        # Predefined modern palettes
        self.modern_sets = [
            {
                "name": "Sunset Vibes",
                "colors": ["#ff512f", "#dd2476", "#f64b64", "#f7914d", "#c41e3a"]
            },
            {
                "name": "Ocean Dreams",
                "colors": ["#36d1dc", "#5b86e5", "#2e4482", "#1b5e91", "#0c2d48"]
            },
            {
                "name": "Forest Fresh",
                "colors": ["#11998e", "#38ef7d", "#1a6b4a", "#2d8b62", "#0f5f3f"]
            }
        ]

    def generate_palette(self, style="Modern", index=0):
        """Generate a color palette visualization.

        Args:
            style: "Modern" or "Luxury"
            index: Palette set index (0-2)

        Returns:
            dict: Contains palette_path, colors, name
        """
        palettes = self.modern_sets if style == "Modern" else self.luxury_sets

        if index >= len(palettes):
            index = 0

        palette_set = palettes[index]
        colors = palette_set["colors"]
        name = palette_set["name"]

        # Create palette visualization (5 color swatches)
        swatch_size = 100
        padding = 10
        width = (swatch_size + padding) * len(colors) + padding
        height = swatch_size + padding * 2

        image = Image.new("RGB", (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(image)

        # Draw color swatches
        for i, color_hex in enumerate(colors):
            x = padding + i * (swatch_size + padding)
            y = padding

            # Convert hex to RGB
            hex_color = color_hex.lstrip("#")
            rgb_color = tuple(int(hex_color[j:j+2], 16) for j in (0, 2, 4))

            # Draw swatch
            draw.rectangle([x, y, x + swatch_size, y + swatch_size], fill=rgb_color)

            # Draw border
            draw.rectangle([x, y, x + swatch_size, y + swatch_size], outline=(100, 100, 100), width=2)

        # Save palette image
        safe_name = "_".join(name.split()) or "palette"
        output_path = os.path.join(self.export_folder, f"{safe_name}.png")

        counter = 1
        base = output_path
        while os.path.exists(output_path):
            name_part, ext = os.path.splitext(base)
            output_path = f"{name_part}_{counter}{ext}"
            counter += 1

        image.save(output_path)

        return {
            "palette_path": output_path,
            "colors": colors,
            "name": name,
            "style": style
        }

    def get_palette_colors(self, style="Modern", index=0):
        """Get color list without generating image.

        Args:
            style: "Modern" or "Luxury"
            index: Palette index

        Returns:
            list: Color hex codes
        """
        palettes = self.modern_sets if style == "Modern" else self.luxury_sets
        if index >= len(palettes):
            index = 0
        return palettes[index]["colors"]

    def get_all_palettes(self):
        """Get all available palettes.

        Returns:
            dict: {"Modern": [...], "Luxury": [...]}
        """
        return {
            "Modern": self.modern_sets,
            "Luxury": self.luxury_sets
        }
