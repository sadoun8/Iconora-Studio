"""
Iconora Studio - Phase 5: Palette Generator
Generates professional color palettes
"""

from PIL import Image, ImageDraw
from pathlib import Path


class PaletteEngine:
    """Generate professional color palettes"""

    # Predefined color palettes
    PALETTES = {
        'Modern': {
            'Sunset Vibes': {
                'colors': ['#FF6B6B', '#FFE66D', '#FF8C42', '#FF5733', '#C92A2A'],
                'description': 'Warm sunset tones',
                'hex': ['#FF6B6B', '#FFE66D', '#FF8C42', '#FF5733', '#C92A2A']
            },
            'Ocean Dreams': {
                'colors': ['#0077B6', '#00D4FF', '#0096C7', '#03045E', '#CAF0F8'],
                'description': 'Cool ocean vibes',
                'hex': ['#0077B6', '#00D4FF', '#0096C7', '#03045E', '#CAF0F8']
            },
            'Forest Fresh': {
                'colors': ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#B7E4C7'],
                'description': 'Natural green tones',
                'hex': ['#2D6A4F', '#40916C', '#52B788', '#74C69D', '#B7E4C7']
            }
        },
        'Luxury': {
            'Gold Elegance': {
                'colors': ['#D4AF37', '#F4E8C1', '#8B7500', '#1A1A1A', '#D4AF37'],
                'description': 'Gold and dark luxury',
                'hex': ['#D4AF37', '#F4E8C1', '#8B7500', '#1A1A1A', '#D4AF37']
            },
            'Silver Supreme': {
                'colors': ['#C0C0C0', '#E8E8E8', '#808080', '#2F2F2F', '#A9A9A9'],
                'description': 'Silver and platinum',
                'hex': ['#C0C0C0', '#E8E8E8', '#808080', '#2F2F2F', '#A9A9A9']
            },
            'Deep Blue Royalty': {
                'colors': ['#003D82', '#0047AB', '#1E40AF', '#1F2937', '#E0E7FF'],
                'description': 'Deep blue royal tones',
                'hex': ['#003D82', '#0047AB', '#1E40AF', '#1F2937', '#E0E7FF']
            }
        }
    }

    def __init__(self):
        """Initialize palette engine"""
        self.palette_width = 300
        self.palette_height = 100
        self.color_box_height = 50

    def _hex_to_rgb(self, hex_color):
        """Convert hex color to RGB tuple"""
        hex_color = hex_color.lstrip('#')
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

    def _rgb_to_hex(self, rgb):
        """Convert RGB tuple to hex string"""
        return '#{:02x}{:02x}{:02x}'.format(rgb[0], rgb[1], rgb[2])

    import colorsys

    def _hsl_to_rgb(self, h, s, l):
        r, g, b = self.colorsys.hls_to_rgb(h, l, s)
        return (int(r * 255), int(g * 255), int(b * 255))

    def _rgb_to_hsl(self, rgb):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = self.colorsys.rgb_to_hls(r, g, b)
        return h, s, l

    def generate_algorithmic_palette(self, base_hex, mode="Analogous"):
        """Generates a 5-color algorithmic palette based on a starting color."""
        base_rgb = self._hex_to_rgb(base_hex)
        h, s, l = self._rgb_to_hsl(base_rgb)

        colors = []
        if mode == "Monochromatic":
            # Vary lightness
            lightnesses = [max(0, min(1, l + d)) for d in [-0.4, -0.2, 0, 0.2, 0.4]]
            colors = [self._rgb_to_hex(self._hsl_to_rgb(h, s, lx)) for lx in lightnesses]

        elif mode == "Analogous":
            # Vary hue slightly
            hues = [(h + d) % 1.0 for d in [-0.1, -0.05, 0, 0.05, 0.1]]
            colors = [self._rgb_to_hex(self._hsl_to_rgb(hx, s, l)) for hx in hues]

        elif mode == "Complementary":
            # Base, complement, and variations
            comp_h = (h + 0.5) % 1.0
            colors = [
                self._rgb_to_hex(base_rgb),
                self._rgb_to_hex(self._hsl_to_rgb(h, s, max(0, l - 0.2))),
                self._rgb_to_hex(self._hsl_to_rgb(comp_h, s, l)),
                self._rgb_to_hex(self._hsl_to_rgb(comp_h, s, min(1, l + 0.2))),
                self._rgb_to_hex(self._hsl_to_rgb(comp_h, s, max(0, l - 0.2))),
            ]

        elif mode == "Triadic":
            h1 = (h + 0.33) % 1.0
            h2 = (h + 0.66) % 1.0
            colors = [
                self._rgb_to_hex(base_rgb),
                self._rgb_to_hex(self._hsl_to_rgb(h1, s, l)),
                self._rgb_to_hex(self._hsl_to_rgb(h1, s, max(0, l - 0.2))),
                self._rgb_to_hex(self._hsl_to_rgb(h2, s, l)),
                self._rgb_to_hex(self._hsl_to_rgb(h2, s, max(0, l - 0.2))),
            ]
        else:
            colors = [base_hex] * 5

        return colors

    def generate_palette(self, style='Modern', palette_name=None, index=None, custom_colors=None):
        """Generate a color palette image and metadata"""
        try:
            if custom_colors:
                colors = custom_colors
                palette_name = palette_name or "Custom Palette"
                desc = "Algorithmic generated palette"
            else:
                if style not in self.PALETTES:
                    raise ValueError(f"Unknown style: {style}")

                style_palettes = self.PALETTES[style]

                # Get palette by name or index
                if palette_name:
                    if palette_name not in style_palettes:
                        raise ValueError(f"Unknown palette: {palette_name}")
                    palette_data = style_palettes[palette_name]
                elif index is not None:
                    palette_names = list(style_palettes.keys())
                    if index >= len(palette_names):
                        raise ValueError(f"Palette index {index} out of range")
                    palette_name = palette_names[index]
                    palette_data = style_palettes[palette_name]
                else:
                    # Return first palette
                    palette_name = list(style_palettes.keys())[0]
                    palette_data = style_palettes[palette_name]

                colors = palette_data['hex']
                desc = palette_data['description']
            color_count = len(colors)
            box_width = self.palette_width // color_count

            image = Image.new('RGB', (self.palette_width, self.palette_height), (255, 255, 255))
            draw = ImageDraw.Draw(image)

            # Draw color boxes
            for i, hex_color in enumerate(colors):
                rgb = self._hex_to_rgb(hex_color)
                x0 = i * box_width
                y0 = 0
                x1 = x0 + box_width
                y1 = self.palette_height

                draw.rectangle([x0, y0, x1, y1], fill=rgb, outline=(200, 200, 200))

                # Draw hex label
                try:
                    from PIL import ImageFont
                    font = ImageFont.load_default()
                    text_bbox = draw.textbbox((0, 0), hex_color, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_x = x0 + (box_width - text_width) // 2
                    text_y = self.palette_height - 20

                    # Choose text color based on brightness
                    brightness = (rgb[0] + rgb[1] + rgb[2]) / 3
                    text_color = (255, 255, 255) if brightness < 128 else (0, 0, 0)

                    draw.text((text_x, text_y), hex_color, fill=text_color, font=font)
                except:
                    pass

            return {
                "palette_path": None,  # To be set when saved
                "colors": colors,
                "name": palette_name,
                "style": style,
                "description": desc,
                "rgb_colors": [self._hex_to_rgb(c) for c in colors],
                "image": image
            }
        except Exception as e:
            raise Exception(f"Failed to generate palette: {str(e)}")

    def get_all_palettes(self):
        """Get list of all available palettes"""
        result = {}
        for style in self.PALETTES:
            result[style] = list(self.PALETTES[style].keys())
        return result

    def get_palette_colors(self, style='Modern', palette_name=None, index=None):
        """Get color list for a palette without generating image"""
        if style not in self.PALETTES:
            raise ValueError(f"Unknown style: {style}")

        style_palettes = self.PALETTES[style]

        if palette_name:
            if palette_name not in style_palettes:
                raise ValueError(f"Unknown palette: {palette_name}")
            palette_data = style_palettes[palette_name]
        elif index is not None:
            palette_names = list(style_palettes.keys())
            if index >= len(palette_names):
                raise ValueError(f"Palette index {index} out of range")
            palette_data = style_palettes[palette_names[index]]
        else:
            palette_data = list(style_palettes.values())[0]

        return {
            "colors": palette_data['hex'],
            "rgb_colors": [self._hex_to_rgb(c) for c in palette_data['hex']],
            "description": palette_data['description']
        }

    def save_palette(self, palette_data, output_path):
        """Save palette image"""
        try:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            palette_data['image'].save(output_path, 'PNG')
            palette_data['palette_path'] = output_path
            return output_path
        except Exception as e:
            raise Exception(f"Failed to save palette: {str(e)}")
