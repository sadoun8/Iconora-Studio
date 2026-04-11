import random
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from core.ai_assistant import AIAssistant

class AILogoEngine:
    """Advanced AI-powered engine for generating professional logos."""

    FONTS = [
        "Arial Bold",
        "Calibri Bold",
        "Segoe UI Bold",
        "Cairo (عربي)",
        "Amiri (عربي)",
        "Reem Kufi (عربي)",
    ]

    COLORS = [
        ("#2563EB", "#60A5FA"), # Blue
        ("#10B981", "#34D399"), # Green
        ("#F59E0B", "#FCD34D"), # Amber
        ("#EF4444", "#F87171"), # Red
        ("#8B5CF6", "#A78BFA"), # Violet
        ("#EC4899", "#F472B6"), # Pink
        ("#06B6D4", "#22D3EE"), # Cyan
        ("#1F2937", "#4B5563")  # Dark Slate
    ]

    ICONS = [
        "rocket", "star", "cube", "lightning", "globe",
        "heart", "cloud", "bolt", "shield", "cog"
    ]

    STYLES = ["modern", "classic", "minimalist", "tech", "elegant"]

    def __init__(self):
        # We will use assets/fonts if available
        self.fonts_dir = os.path.join(os.getcwd(), "assets", "fonts")
        self.assistant = AIAssistant()

    def generate(self, text, style="modern", candidate_fonts=None):
        """Generates a logo configuration based on AI logic."""
        fonts_pool = candidate_fonts or self.FONTS
        if not fonts_pool:
            fonts_pool = ["Arial Bold"]

        # Re-load assistant each call to pick latest settings (endpoint/model/enabled)
        self.assistant = AIAssistant()

        try:
            data = self.assistant.suggest_logo(
                text=text,
                style=style,
                candidate_fonts=fonts_pool,
            )
            # keep compatibility fields used by UI
            data["icon"] = random.choice(self.ICONS)
            data["timestamp"] = None
            return data
        except Exception:
            font = random.choice(fonts_pool)
            colors = random.choice(self.COLORS)
            icon = random.choice(self.ICONS)
            layout = random.choice(["vertical", "horizontal", "stacked"])

            return {
                "text": text,
                "font": font,
                "colors": colors,
                "icon": icon,
                "style": style,
                "layout": layout,
                "timestamp": None # Placeholder
            }

    def render_preview(self, data, size=(600, 400)):
        """Renders a PIL image preview of the AI generated logo."""
        width, height = size
        img = Image.new("RGBA", size, (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)

        # Gradient background (simplified)
        c1, c2 = data["colors"]

        # Draw some abstract background elements based on style
        if data["style"] == "tech":
            for _ in range(10):
                x = random.randint(0, width)
                y = random.randint(0, height)
                draw.rectangle([x, y, x+10, y+10], outline=c1, width=1)

        # Center coordinates
        cx, cy = width // 2, height // 2

        # Draw Icon Placeholder
        icon_size = 60
        draw.ellipse([cx - icon_size, cy - 100, cx + icon_size, cy - 100 + icon_size*2], outline=c1, width=4)

        # Draw Text
        # Note: In a real implementation, we'd load actual fonts from assets/
        try:
            # Try to load a font, fallback to default
            f_size = 48
            font_obj = ImageFont.load_default()
        except:
            font_obj = ImageFont.load_default()

        text = data["text"]
        draw.text((cx, cy + 40), text, fill=c1, font=font_obj, anchor="mm")

        return img
