from PIL import Image, ImageDraw, ImageFilter
import math

class GradientEngine:
    """Professional Gradient Engine for Iconora Studio 3.0."""

    def linear(self, width, height, c1, c2, direction="vertical"):
        """Generates a linear gradient between two colors."""
        img = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(img)

        # Ensure input colors are RGB/RGBA tuples
        if isinstance(c1, str) and c1.startswith('#'):
            c1 = self._hex_to_rgb(c1)
        if isinstance(c2, str) and c2.startswith('#'):
            c2 = self._hex_to_rgb(c2)

        for i in range(height if direction == "vertical" else width):
            # Interpolate RGB
            ratio = i / (height if direction == "vertical" else width)
            r = int(c1[0] + (c2[0] - c1[0]) * ratio)
            g = int(c1[1] + (c2[1] - c1[1]) * ratio)
            b = int(c1[2] + (c2[2] - c1[2]) * ratio)
            a = int((c1[3] if len(c1) > 3 else 255) + 
                    ((c2[3] if len(c2) > 3 else 255) - (c1[3] if len(c1) > 3 else 255)) * ratio)
            
            if direction == "vertical":
                draw.line([(0, i), (width, i)], fill=(r, g, b, a))
            else:
                draw.line([(i, 0), (i, height)], fill=(r, g, b, a))
                
        return img

    def radial(self, width, height, c1, c2, center=None):
        """Generates a radial gradient between two colors."""
        img = Image.new("RGBA", (width, height))
        draw = ImageDraw.Draw(img)
        
        cx, cy = center if center else (width // 2, height // 2)
        max_dist = math.sqrt(max(cx, width-cx)**2 + max(cy, height-cy)**2)

        if isinstance(c1, str) and c1.startswith('#'):
            c1 = self._hex_to_rgb(c1)
        if isinstance(c2, str) and c2.startswith('#'):
            c2 = self._hex_to_rgb(c2)

        for y in range(height):
            for x in range(width):
                dist = math.sqrt((x - cx)**2 + (y - cy)**2)
                ratio = min(1.0, dist / max_dist)
                
                r = int(c1[0] + (c2[0] - c1[0]) * ratio)
                g = int(c1[1] + (c2[1] - c1[1]) * ratio)
                b = int(c1[2] + (c2[2] - c1[2]) * ratio)
                a = int((c1[3] if len(c1) > 3 else 255) + 
                        ((c2[3] if len(c2) > 3 else 255) - (c1[3] if len(c1) > 3 else 255)) * ratio)
                
                img.putpixel((x, y), (r, g, b, a))
                
        return img

    def conic(self, width, height, c1, c2, center=None):
        """Generates a conic (angular) gradient between two colors."""
        img = Image.new("RGBA", (width, height))
        cx, cy = center if center else (width // 2, height // 2)
        
        if isinstance(c1, str) and c1.startswith('#'):
            c1 = self._hex_to_rgb(c1)
        if isinstance(c2, str) and c2.startswith('#'):
            c2 = self._hex_to_rgb(c2)

        for y in range(height):
            for x in range(width):
                angle = math.atan2(y - cy, x - cx)
                ratio = (angle + math.pi) / (2 * math.pi)
                
                r = int(c1[0] + (c2[0] - c1[0]) * ratio)
                g = int(c1[1] + (c2[1] - c1[1]) * ratio)
                b = int(c1[2] + (c2[2] - c1[2]) * ratio)
                a = int((c1[3] if len(c1) > 3 else 255) + 
                        ((c2[3] if len(c2) > 3 else 255) - (c1[3] if len(c1) > 3 else 255)) * ratio)
                
                img.putpixel((x, y), (r, g, b, a))
                
        return img

    def _hex_to_rgb(self, hex_color):
        hex_color = hex_color.lstrip('#')
        if len(hex_color) == 6:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        elif len(hex_color) == 8:
            return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4, 6))
        return (0, 0, 0)
