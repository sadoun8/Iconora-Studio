from __future__ import annotations

from pathlib import Path

from config import APP_PHASE, APP_VERSION, FONTS_DIR

from backend.services.settings_service import load_settings


GENERAL_FONTS = [
    {"label": "Cairo (Modern Arabic)", "value": "Cairo"},
    {"label": "Tajawal", "value": "Tajawal"},
    {"label": "Amiri", "value": "Amiri"},
    {"label": "IBM Plex Sans Arabic", "value": "IBM Plex Sans Arabic"},
    {"label": "Scheherazade New", "value": "Scheherazade New"},
    {"label": "Noto Naskh Arabic", "value": "Noto Naskh Arabic"},
    {"label": "Outfit", "value": "Outfit"},
    {"label": "Arial", "value": "Arial"},
    {"label": "Georgia", "value": "Georgia"},
    {"label": "Courier New", "value": "Courier New"},
]

SIGNATURE_FONTS = [
    {"label": "Amiri", "value": "Amiri"},
    {"label": "Scheherazade New", "value": "Scheherazade New"},
    {"label": "Noto Naskh Arabic", "value": "Noto Naskh Arabic"},
    {"label": "Cairo", "value": "Cairo"},
    {"label": "Georgia", "value": "Georgia"},
    {"label": "Courier New", "value": "Courier New"},
]

LOGO_TEMPLATES = [
    {
        "id": "coffee", "label": "مقهى", "emoji": "☕", "bg": "#2d1b0e",
        "objects": [
            {"type": "rect", "fill": "#c8860a", "rx": 70, "ry": 70, "width": 320, "height": 320, "left": 240, "top": 240},
            {"type": "text", "text": "مَقهى", "fontSize": 80, "fontFamily": "Amiri", "fill": "#fff", "left": 270, "top": 288, "fontWeight": "bold"},
            {"type": "text", "text": "C A F É", "fontSize": 20, "fontFamily": "Outfit", "fill": "#c8860a", "left": 318, "top": 420, "charSpacing": 250},
        ],
    },
    {
        "id": "tech", "label": "تقنية", "emoji": "⚡", "bg": "#0d0d1f",
        "objects": [
            {"type": "rect", "fill": "transparent", "stroke": "#6366f1", "strokeWidth": 3, "rx": 16, "ry": 16, "width": 340, "height": 120, "left": 230, "top": 310},
            {"type": "text", "text": "TECH", "fontSize": 68, "fontFamily": "Outfit", "fill": "#818cf8", "left": 265, "top": 316, "fontWeight": "800"},
            {"type": "text", "text": "نصنع المستقبل", "fontSize": 22, "fontFamily": "Cairo", "fill": "#64748b", "left": 280, "top": 450},
        ],
    },
    {
        "id": "elegant", "label": "أناقة", "emoji": "✨", "bg": "#080808",
        "objects": [
            {"type": "text", "text": "LUXE", "fontSize": 96, "fontFamily": "Georgia", "fill": "#c9a227", "left": 230, "top": 310, "fontWeight": "bold"},
            {"type": "text", "text": "— النخبـة —", "fontSize": 26, "fontFamily": "Amiri", "fill": "#64748b", "left": 290, "top": 435},
        ],
    },
    {
        "id": "minimal", "label": "مينيمال", "emoji": "◻", "bg": "#f8fafc",
        "objects": [
            {"type": "rect", "fill": "#0f1115", "rx": 10, "ry": 10, "width": 340, "height": 100, "left": 230, "top": 350},
            {"type": "text", "text": "BRAND", "fontSize": 50, "fontFamily": "Outfit", "fill": "#ffffff", "left": 265, "top": 368, "fontWeight": "700", "charSpacing": 200},
        ],
    },
    {
        "id": "sports", "label": "رياضة", "emoji": "🏆", "bg": "#0a1628",
        "objects": [
            {"type": "rect", "fill": "#f59e0b", "rx": 0, "ry": 0, "width": 400, "height": 12, "left": 200, "top": 390},
            {"type": "text", "text": "CHAMPIONS", "fontSize": 54, "fontFamily": "Outfit", "fill": "#ffffff", "left": 200, "top": 310, "fontWeight": "800", "charSpacing": 80},
            {"type": "text", "text": "أبطال", "fontSize": 40, "fontFamily": "Cairo", "fill": "#f59e0b", "left": 320, "top": 415, "fontWeight": "bold"},
        ],
    },
    {
        "id": "restaurant", "label": "مطعم", "emoji": "🍽️", "bg": "#1a0a04",
        "objects": [
            {"type": "circle", "fill": "transparent", "stroke": "#b45309", "strokeWidth": 4, "radius": 160, "left": 240, "top": 240},
            {"type": "text", "text": "مطعــم", "fontSize": 62, "fontFamily": "Amiri", "fill": "#fbbf24", "left": 280, "top": 318, "fontWeight": "bold"},
            {"type": "text", "text": "RESTAURANT", "fontSize": 16, "fontFamily": "Outfit", "fill": "#b45309", "left": 263, "top": 407, "charSpacing": 180},
        ],
    },
    {
        "id": "studio", "label": "استوديو", "emoji": "🎨", "bg": "#0f0520",
        "objects": [
            {"type": "rect", "fill": "#7c3aed", "rx": 50, "ry": 50, "width": 120, "height": 120, "left": 340, "top": 240},
            {"type": "text", "text": "STUDIO", "fontSize": 56, "fontFamily": "Outfit", "fill": "#ffffff", "left": 248, "top": 385, "fontWeight": "800", "charSpacing": 120},
            {"type": "text", "text": "تصميم إبداعي", "fontSize": 20, "fontFamily": "Cairo", "fill": "#a78bfa", "left": 295, "top": 455},
        ],
    },
    {
        "id": "medical", "label": "طب", "emoji": "⚕️", "bg": "#f0fdf4",
        "objects": [
            {"type": "circle", "fill": "#16a34a", "radius": 100, "left": 300, "top": 200},
            {"type": "rect", "fill": "#ffffff", "rx": 4, "ry": 4, "width": 30, "height": 100, "left": 370, "top": 250},
            {"type": "rect", "fill": "#ffffff", "rx": 4, "ry": 4, "width": 100, "height": 30, "left": 335, "top": 285},
            {"type": "text", "text": "عيادة الشفاء", "fontSize": 38, "fontFamily": "Cairo", "fill": "#15803d", "left": 275, "top": 440, "fontWeight": "bold"},
        ],
    },
]


ICON_TEMPLATES = [
    {
        "id": "app-icon",
        "label": "تطبيق",
        "emoji": "📱",
        "bg": "#6366f1",
        "objects": [
            {"type": "rect", "fill": "rgba(255,255,255,0.15)", "rx": 80, "ry": 80, "width": 340, "height": 340, "left": 85, "top": 85},
            {"type": "text", "text": "A", "fontSize": 220, "fontFamily": "Outfit", "fill": "#ffffff", "left": 155, "top": 120, "fontWeight": "800"},
        ],
    },
    {
        "id": "shield",
        "label": "أمان",
        "emoji": "🛡️",
        "bg": "#0f172a",
        "objects": [
            {"type": "circle", "fill": "#3b82f6", "radius": 160, "left": 96, "top": 96},
            {"type": "text", "text": "✓", "fontSize": 200, "fontFamily": "Outfit", "fill": "#ffffff", "left": 145, "top": 110, "fontWeight": "700"},
        ],
    },
    {
        "id": "leaf-icon",
        "label": "طبيعة",
        "emoji": "🌿",
        "bg": "#052e16",
        "objects": [
            {"type": "circle", "fill": "#16a34a", "radius": 180, "left": 80, "top": 80},
            {"type": "text", "text": "🌿", "fontSize": 220, "fontFamily": "Outfit", "fill": "#ffffff", "left": 90, "top": 100},
        ],
    },
]

SIGNATURE_TEMPLATES = [
    {
        "id": "sig-classic",
        "label": "كلاسيكي",
        "emoji": "✍️",
        "bg": "#fffef7",
        "objects": [
            {"type": "text", "text": "اسمك هنا", "fontSize": 90, "fontFamily": "Amiri", "fill": "#0f1115", "left": 120, "top": 80, "fontWeight": "bold", "fontStyle": "italic"},
            {"type": "rect", "fill": "#0f1115", "rx": 0, "ry": 0, "width": 560, "height": 3, "left": 120, "top": 195},
        ],
    },
    {
        "id": "sig-modern",
        "label": "عصري",
        "emoji": "🖋️",
        "bg": "#0f1115",
        "objects": [
            {"type": "text", "text": "YOUR NAME", "fontSize": 70, "fontFamily": "Outfit", "fill": "#ffffff", "left": 150, "top": 80, "fontWeight": "800", "charSpacing": 120},
            {"type": "rect", "fill": "#6366f1", "rx": 6, "ry": 6, "width": 80, "height": 6, "left": 150, "top": 180},
            {"type": "text", "text": "Designer & Creator", "fontSize": 24, "fontFamily": "Outfit", "fill": "#64748b", "left": 150, "top": 210},
        ],
    },
    {
        "id": "sig-gold",
        "label": "ذهبي",
        "emoji": "✨",
        "bg": "#0a0804",
        "objects": [
            {"type": "text", "text": "الاسم بالعربية", "fontSize": 80, "fontFamily": "Amiri", "fill": "#c9a227", "left": 80, "top": 70, "fontWeight": "bold"},
            {"type": "rect", "fill": "transparent", "stroke": "#c9a227", "strokeWidth": 2, "rx": 0, "ry": 0, "width": 640, "height": 240, "left": 80, "top": 30},
        ],
    },
]

SECTION_ICONS = {
    "logo": [
        {"label": "نجمة", "emoji": "⭐", "svg": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"},
        {"label": "قلب", "emoji": "❤", "svg": "M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"},
        {"label": "برق", "emoji": "⚡", "svg": "M13 2L3 14h9l-1 8 10-12h-9l1-8z"},
        {"label": "خاتم", "emoji": "💎", "svg": "M6 2l-4 6 10 14L22 8l-4-6H6zM3.43 8L6.37 4h11.26l2.94 4H3.43zm8.57 11.8L4.56 10h14.88L12 19.8z"},
        {"label": "شعلة", "emoji": "🔥", "svg": "M13.5 0.67s.74 2.65.74 4.8c0 2.06-1.35 3.73-3.41 3.73-2.07 0-3.63-1.67-3.63-3.73l.03-.36C5.21 7.51 4 10.62 4 14c0 4.42 3.58 8 8 8s8-3.58 8-8C20 8.61 17.41 3.8 13.5.67z"},
        {"label": "ورقة", "emoji": "🍃", "svg": "M17 8C8 10 5.9 16.17 3.82 21.34L5.71 22l1-2.3A4.49 4.49 0 0 0 8 20C19 20 22 3 22 3c-1 2-8 2-8 2z"},
        {"label": "هلال", "emoji": "🌙", "svg": "M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"},
        {"label": "عين", "emoji": "👁", "svg": "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zm11 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"},
        {"label": "جبل", "emoji": "⛰️", "svg": "M3 17l6-12 4 7 2.5-4L21 17H3z"},
        {"label": "اللانهاية", "emoji": "∞", "svg": "M18.6 6.62c-1.44 0-2.8.56-3.77 1.53L12 10.66 10.48 12h.01L7.8 14.39c-.64.64-1.49.99-2.4.99-1.87 0-3.39-1.51-3.39-3.38S3.53 8.62 5.4 8.62c.91 0 1.76.35 2.44 1.03l1.13 1 1.51-1.34L9.22 8.2C8.2 7.18 6.84 6.62 5.4 6.62 2.42 6.62 0 9.04 0 12s2.42 5.38 5.4 5.38c1.44 0 2.8-.56 3.77-1.53l2.83-2.51.01.01L13.52 12h-.01l2.69-2.39c.64-.64 1.49-.99 2.4-.99 1.87 0 3.39 1.51 3.39 3.38s-1.52 3.38-3.39 3.38c-.9 0-1.76-.35-2.44-1.03l-1.14-1.01-1.51 1.34 1.27 1.12c1.02 1.01 2.37 1.57 3.82 1.57 2.98 0 5.4-2.41 5.4-5.38s-2.42-5.38-5.4-5.38z"},
        {"label": "موجة", "emoji": "🌊", "svg": "M2 8c1.5-2 3-2 4.5 0s3 2 4.5 0 3-2 4.5 0 3 2 4.5 0M2 14c1.5-2 3-2 4.5 0s3 2 4.5 0 3-2 4.5 0 3 2 4.5 0"},
        {"label": "صاروخ", "emoji": "🚀", "svg": "M12 2.5s4 2 5.5 8-2 10.5-5.5 11-5.5-1-7-5.5S5 7.5 12 2.5z M9 11h6M10 14h4"},
    ],
    "icon": [
        {"label": "نجمة", "emoji": "⭐", "svg": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"},
        {"label": "قلب", "emoji": "❤", "svg": "M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"},
        {"label": "برق", "emoji": "⚡", "svg": "M13 2L3 14h9l-1 8 10-12h-9l1-8z"},
        {"label": "هلال", "emoji": "🌙", "svg": "M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"},
        {"label": "عين", "emoji": "👁", "svg": "M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8zm11 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6z"},
        {"label": "علامة", "emoji": "✓", "svg": "M20 6L9 17l-5-5"},
        {"label": "موجة", "emoji": "〰", "svg": "M2 12C4 8 6 6 8 8s4 6 6 4 4-6 6-4"},
        {"label": "X", "emoji": "✖", "svg": "M18 6L6 18M6 6l12 12"},
    ],
    "signature": [
        {"label": "قلم", "emoji": "✒️", "svg": "M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"},
        {"label": "بريد", "emoji": "✉️", "svg": "M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2zm0 2l8 5 8-5"},
        {"label": "هاتف", "emoji": "📞", "svg": "M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 13 19.79 19.79 0 0 1 1.61 4.4 2 2 0 0 1 3.59 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L7.91 9.91a16 16 0 0 0 6.16 6.16l.91-.91a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"},
        {"label": "موقع", "emoji": "🌐", "svg": "M12 2a10 10 0 1 0 0 20A10 10 0 0 0 12 2zm0 0c-2.76 4-2.76 16 0 16m0 0c2.76-4 2.76-16 0-16M2 12h20"},
        {"label": "نجمة", "emoji": "⭐", "svg": "M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"},
    ],
}

ORNAMENTS = [
    {"label": "درع فيكتوري", "emoji": "🛡️", "svg": "M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zM12 6c-3.31 0-6 2.69-6 6s2.69 6 6 6 6-2.69 6-6-2.69-6-6-6zm0 10c-2.21 0-4-1.79-4-4s1.79-4 4-4 4 1.79 4 4-1.79 4-4 4z"},
    {"label": "غار روكوكو", "emoji": "🌿", "svg": "M21.58 12c0-5.3-4.3-9.58-9.58-9.58C6.7 2.42 2.42 6.7 2.42 12S6.7 21.58 12 21.58c5.3 0 9.58-4.3 9.58-9.58zM12 20.42c-4.64 0-8.42-3.78-8.42-8.42 0-4.64 3.78-8.42 8.42-8.42s8.42 3.78 8.42 8.42c0 4.64-3.78 8.42-8.42 8.42z"},
    {"label": "زخرفة لوتس", "emoji": "🪷", "svg": "M12 2C9.24 2 7 4.24 7 7c0 2.21 1.43 4.08 3.42 4.74C8.61 14.28 6.51 16 4 16v2c3.48 0 6.43-2.18 7.57-5.26.14.3.3.59.43.9V22h2v-8.36c.13-.31.29-.6.43-.9C15.57 15.82 18.52 18 22 18v-2c-2.51 0-4.61-1.72-6.42-4.26C17.57 11.08 19 9.21 19 7c0-2.76-2.24-5-5-5zm-3 5c0-1.66 1.34-3 3-3s3 1.34 3 3-1.34 3-3 3-3-1.34-3-3z"},
    {"label": "إكليل", "emoji": "🍀", "svg": "M12 21.58c-5.3 0-9.58-4.3-9.58-9.58C2.42 6.7 6.7 2.42 12 2.42c5.3 0 9.58 4.3 9.58 9.58 0 5.3-4.3 9.58-9.58 9.58zm0-17.16c-4.18 0-7.58 3.4-7.58 7.58 0 4.18 3.4 7.58 7.58 7.58s7.58-3.4 7.58-7.58c0-4.18-3.4-7.58-7.58-7.58z M12 6.5a5.5 5.5 0 0 0-5.5 5.5c0 3.03 2.47 5.5 5.5 5.5s5.5-2.47 5.5-5.5A5.5 5.5 0 0 0 12 6.5zm0 9c-1.93 0-3.5-1.57-3.5-3.5S10.07 8.5 12 8.5s3.5 1.57 3.5 3.5-1.57 3.5-3.5 3.5z"},
    {"label": "وسام", "emoji": "🏅", "svg": "M12 2L9.5 4.5 6 4l-1 3.5L2 9.5 4 12l-2 2.5 3.5 2L6 20l3.5-.5L12 22l2.5-2.5L18 20l1-3.5L22 14.5 20 12l2-2.5-3.5-2L18 4l-3.5.5L12 2zm0 16c-3.31 0-6-2.69-6-6s2.69-6 6-6 6 2.69 6 6-2.69 6-6 6z M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"},
    {"label": "زخرفة أرابيسك", "emoji": "✨", "svg": "M12 0c1.33 4.37 4.63 7.67 9 9-4.37 1.33-7.67 4.63-9 9-1.33-4.37-4.63-7.67-9-9 4.37-1.33 7.67-4.63 9-9z"},
    {"label": "فاصل أميري", "emoji": "〰", "svg": "M2 12c1.5 2.5 3.5 4.5 6 4s4.5-1.5 6-4-1.5-4.5-4-6-6-2-8 0-4 4.5-2 8z M14 12c1.5 2.5 3.5 4.5 6 4s4.5-1.5 6-4-1.5-4.5-4-6-6-2-8 0-4 4.5-2 8z M12 12h2 M10 12h2"},
]

SECTION_SIZES = {
    "logo": [
        {"label": "مربع 800x800", "w": 800, "h": 800},
        {"label": "أفقي 1200x600", "w": 1200, "h": 600},
        {"label": "عمودي 600x900", "w": 600, "h": 900},
        {"label": "شعار 512x512", "w": 512, "h": 512},
    ],
    "icon": [
        {"label": "App Icon 512x512", "w": 512, "h": 512},
        {"label": "Favicon 32x32", "w": 32, "h": 32},
        {"label": "Icon 128x128", "w": 128, "h": 128},
        {"label": "Icon 256x256", "w": 256, "h": 256},
    ],
    "signature": [
        {"label": "توقيع 800x300", "w": 800, "h": 300},
        {"label": "توقيع 600x200", "w": 600, "h": 200},
        {"label": "مربع 400x400", "w": 400, "h": 400},
        {"label": "بانر 1200x400", "w": 1200, "h": 400},
    ],
}


def _font_assets() -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    if FONTS_DIR.exists():
        for file in sorted(FONTS_DIR.iterdir()):
            if file.suffix.lower() in {".ttf", ".otf"}:
                results.append({"label": file.stem.replace("-", " "), "value": file.stem})
    return results


def get_bootstrap_assets() -> dict:
    settings = load_settings()
    asset_fonts = _font_assets()
    general_fonts = GENERAL_FONTS + [font for font in asset_fonts if font["value"] not in {item["value"] for item in GENERAL_FONTS}]
    signature_fonts = SIGNATURE_FONTS + [font for font in asset_fonts if font["value"] not in {item["value"] for item in SIGNATURE_FONTS}]
    return {
        "fonts": {
            "general": general_fonts,
            "signature": signature_fonts,
        },
        "templates": {
            "logo": LOGO_TEMPLATES,
            "icon": ICON_TEMPLATES,
            "signature": SIGNATURE_TEMPLATES,
        },
        "icons": SECTION_ICONS,
        "ornaments": ORNAMENTS,
        "sizes": SECTION_SIZES,
        "ai_hints": {
            "icon": 'مثال: أيقونة تطبيق بتصميم مسطح، رمز البرق الأزرق على خلفية داكنة',
            "signature": 'مثال: توقيع إلكتروني أنيق باسم "محمد" بخط عربي ذهبي على خلفية داكنة',
            "logo": 'مثال: أسد هادئ بأسلوب فيكتور مسطح لشركة تقنية، لا نص',
        },
        "settings": {
            "app_version": APP_VERSION,
            "app_phase": APP_PHASE,
            "ai_enabled": bool(settings.get("ai_enabled", True)),
            "language": settings.get("language", "en"),
            "theme": settings.get("theme", "dark"),
        },
    }
