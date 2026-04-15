import base64
import random
import re
from threading import Lock

from fastapi import APIRouter, HTTPException
import requests

from backend.schemas.ai_models import LogoGenerationDebug, LogoGenerationResponse, LogoRequest

router = APIRouter()
rembg_session = None
rembg_session_lock = Lock()
remove = None
new_session = None

ALLOWED_SECTIONS = {"logo", "icon", "signature"}
INVISIBLE_PROMPT_CHARS = "\u00ad\u200b\u200c\u200d\u200e\u200f\u2060\ufeff"

PROMPT_PREFIXES = [
    "design a logo for",
    "create a logo for",
    "generate a logo for",
    "logo for",
    "design an icon for",
    "create an icon for",
    "generate an icon for",
    "icon for",
    "design a signature for",
    "create a signature for",
    "generate a signature for",
    "signature for",
    "\u062a\u0635\u0645\u064a\u0645 \u0634\u0639\u0627\u0631",
    "\u0635\u0645\u0645 \u0634\u0639\u0627\u0631",
    "\u0623\u0646\u0634\u0626 \u0634\u0639\u0627\u0631",
    "\u0627\u0646\u0634\u0626 \u0634\u0639\u0627\u0631",
    "\u062a\u0635\u0645\u064a\u0645 \u0623\u064a\u0642\u0648\u0646\u0629",
    "\u0635\u0645\u0645 \u0623\u064a\u0642\u0648\u0646\u0629",
    "\u0623\u0646\u0634\u0626 \u0623\u064a\u0642\u0648\u0646\u0629",
    "\u0627\u0646\u0634\u0626 \u0623\u064a\u0642\u0648\u0646\u0629",
    "\u062a\u0635\u0645\u064a\u0645 \u062a\u0648\u0642\u064a\u0639",
    "\u0635\u0645\u0645 \u062a\u0648\u0642\u064a\u0639",
    "\u0623\u0646\u0634\u0626 \u062a\u0648\u0642\u064a\u0639",
    "\u0627\u0646\u0634\u0626 \u062a\u0648\u0642\u064a\u0639",
    "\u062a\u0648\u0642\u064a\u0639 \u0628\u0627\u0633\u0645",
    "\u062a\u0648\u0642\u064a\u0639 \u0639\u0631\u0628\u064a \u0628\u0627\u0633\u0645",
    "\u062a\u0648\u0642\u064a\u0639 \u0627\u0644\u0643\u062a\u0631\u0648\u0646\u064a \u0628\u0627\u0633\u0645",
]

PROMPT_CLEANUP_PHRASES = [
    "\u0628\u062e\u0637 \u0639\u0631\u0628\u064a",
    "\u0628\u0627\u0644\u062e\u0637 \u0627\u0644\u0639\u0631\u0628\u064a",
    "\u0628\u0627\u0644\u0639\u0631\u0628\u064a",
    "arabic calligraphy",
    "in arabic",
]

SIGNATURE_NOISE_PATTERNS = [
    r"\bsignature\b",
    r"\bhandwritten\b",
    r"\bcalligraphy\b",
    r"\bfor\b",
    "\u062a\u0648\u0642\u064a\u0639",
    "\u0628\u0627\u0633\u0645",
    "\u0627\u0633\u0645",
    "\u0628\u0627\u0644\u0627\u0633\u0645",
]

SIGNATURE_STYLE_KEYWORDS = [
    (["arabic", "\u0639\u0631\u0628\u064a", "\u0639\u0631\u0628\u0649"], "authentic Arabic calligraphy styling"),
    (["electronic", "digital", "\u0627\u0644\u0643\u062a\u0631\u0648\u0646\u064a", "\u0631\u0642\u0645\u064a"], "modern electronic signature aesthetic"),
    (["elegant", "luxury", "luxurious", "\u0623\u0646\u064a\u0642", "\u0641\u0627\u062e\u0631"], "elegant premium presentation"),
    (["ornate", "decorative", "flourish", "\u0645\u0632\u062e\u0631\u0641", "\u0632\u062e\u0631\u0641\u064a"], "ornate decorative flourishes"),
    (["minimal", "simple", "\u0628\u0633\u064a\u0637"], "minimal clean styling"),
    (["bold", "\u0639\u0631\u064a\u0636"], "bold confident strokes"),
    (["classic", "\u0643\u0644\u0627\u0633\u064a\u0643\u064a"], "classic timeless character"),
]

ARABIC_BACKGROUND_PATTERNS = [
    (
        "dark",
        re.compile(
            r"(?:\u0639\u0644\u0649|\u0628)?\s*(?:\u062e\u0644\u0641\u064a(?:\u0629|\u0647))\s+"
            r"(?:\u062f\u0627\u0643\u0646(?:\u0629)?|\u0633\u0648\u062f\u0627\u0621|\u0633\u0648\u062f\u0627|\u0641\u062d\u0645\u064a(?:\u0629)?)"
        ),
        "dark charcoal background",
        "high contrast bright white or silver ink",
        True,
    ),
    (
        "light",
        re.compile(
            r"(?:\u0639\u0644\u0649|\u0628)?\s*(?:\u062e\u0644\u0641\u064a(?:\u0629|\u0647))\s+"
            r"(?:\u0641\u0627\u062a\u062d(?:\u0629)?|\u0628\u064a\u0636\u0627\u0621|\u0628\u064a\u0636\u0627|\u0643\u0631\u064a\u0645\u064a(?:\u0629)?)"
        ),
        "soft light background",
        "high contrast black ink",
        True,
    ),
    (
        "transparent",
        re.compile(
            r"(?:\u062e\u0644\u0641\u064a(?:\u0629|\u0647))\s+"
            r"(?:\u0634\u0641\u0627\u0641(?:\u0629)?|\u0628\u062f\u0648\u0646)"
        ),
        "transparent isolated background",
        "high contrast black ink",
        False,
    ),
]

ENGLISH_BACKGROUND_PATTERNS = [
    ("dark", re.compile(r"(?:on|with)\s+(?:a\s+)?(?:dark|black|charcoal)\s+background", re.IGNORECASE), "dark charcoal background", "high contrast bright white or silver ink", True),
    ("light", re.compile(r"(?:on|with)\s+(?:a\s+)?(?:light|white|cream)\s+background", re.IGNORECASE), "soft light background", "high contrast black ink", True),
    ("transparent", re.compile(r"(?:on|with)\s+(?:a\s+)?transparent\s+background", re.IGNORECASE), "transparent isolated background", "high contrast black ink", False),
]


def normalize_prompt_text(text: str | None) -> str:
    if not text:
        return ""
    cleaned = str(text).translate({ord(char): None for char in INVISIBLE_PROMPT_CHARS})
    return re.sub(r"\s+", " ", cleaned).strip()


def normalize_section(section: str | None) -> str:
    return section if section in ALLOWED_SECTIONS else "logo"


def contains_arabic(text: str | None) -> bool:
    return any("\u0600" <= char <= "\u06FF" for char in (text or ""))


def sanitize_prompt(text: str) -> str:
    cleaned = normalize_prompt_text(text)
    if not cleaned:
        return cleaned

    lowered = cleaned.lower()
    for prefix in PROMPT_PREFIXES:
        if lowered.startswith(prefix):
            cleaned = cleaned[len(prefix):].strip(" :,-")
            break

    for phrase in PROMPT_CLEANUP_PHRASES:
        cleaned = re.sub(re.escape(phrase), "", cleaned, flags=re.IGNORECASE).strip(" :,-")

    return normalize_prompt_text(cleaned)[:260]


def wants_arabic_script(prompt: str, original_prompt: str) -> bool:
    prompt_text = normalize_prompt_text(prompt).lower()
    original_text = normalize_prompt_text(original_prompt).lower()
    return (
        contains_arabic(original_prompt)
        or contains_arabic(prompt)
        or "arabic" in prompt_text
        or "arabic" in original_text
        or "\u0628\u0627\u0644\u0639\u0631\u0628\u064a" in original_text
        or "\u0628\u0627\u0644\u0639\u0631\u0628\u064a" in prompt_text
        or "\u0628\u062e\u0637 \u0639\u0631\u0628\u064a" in original_text
        or "\u0628\u062e\u0637 \u0639\u0631\u0628\u064a" in prompt_text
    )


def translate_for_description(text: str) -> str:
    """
    Translate descriptive text to English when helpful.
    Signature names themselves should not be translated.
    """
    try:
        if contains_arabic(text):
            try:
                from deep_translator import GoogleTranslator

                translator = GoogleTranslator(source="auto", target="en")
                translated = translator.translate(text)
                print(f"Translated '{text}' to '{translated}' for AI description")
                return translated
            except ImportError:
                print("deep-translator not found. Arabic translation will be skipped.")
                return text
        return text
    except Exception as error:
        print(f"Translation failed: {error}")
        return text


def get_generation_dimensions(section: str) -> tuple[int, int]:
    if normalize_section(section) == "signature":
        return (1536, 768)
    return (1024, 1024)


def cleanup_signature_name(candidate: str) -> str:
    cleaned = normalize_prompt_text(candidate)
    boundary_patterns = [
        r"\s+(?:\u0639\u0644\u0649|\u0628)?\s*(?:\u062e\u0644\u0641\u064a(?:\u0629|\u0647)).*$",
        r"\s+(?:on|with)\s+(?:a\s+)?(?:dark|light|white|black|charcoal|transparent)\s+background.*$",
    ]
    for pattern in boundary_patterns:
        cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE).strip(" ,.;:-")
    return normalize_prompt_text(cleaned)[:80]


def extract_signature_name(prompt: str) -> tuple[str, str]:
    normalized = normalize_prompt_text(prompt)
    name_patterns = [
        r"(?:\u0628\u0627\u0633\u0645|\u0628\u0627\u0644\u0627\u0633\u0645|\u0627\u0633\u0645)\s+(.+)",
        r"(?:name|named|for)\s+(.+)",
    ]

    for pattern in name_patterns:
        match = re.search(pattern, normalized, flags=re.IGNORECASE)
        if not match:
            continue
        name = cleanup_signature_name(match.group(1))
        if not name:
            continue
        phrase = match.group(0)
        remainder = normalize_prompt_text(normalized.replace(phrase, " "))
        return name, remainder

    fallback = sanitize_prompt(normalized)
    fallback = cleanup_signature_name(fallback)
    return fallback or "the name", normalized


def detect_signature_background(prompt: str) -> tuple[str | None, str, str, bool, str]:
    normalized = normalize_prompt_text(prompt)

    for label, pattern, background_prompt, ink_prompt, keep_background in ARABIC_BACKGROUND_PATTERNS:
        match = pattern.search(normalized)
        if match:
            return label, background_prompt, ink_prompt, keep_background, match.group(0)

    for label, pattern, background_prompt, ink_prompt, keep_background in ENGLISH_BACKGROUND_PATTERNS:
        match = pattern.search(normalized)
        if match:
            return label, background_prompt, ink_prompt, keep_background, match.group(0)

    return None, "plain white background", "high contrast black ink", False, ""


def build_signature_style_hint(prompt: str, display_name: str, background_phrase: str) -> tuple[str | None, str]:
    working = normalize_prompt_text(prompt)
    if display_name:
        working = re.sub(re.escape(display_name), " ", working, flags=re.IGNORECASE)
    if background_phrase:
        working = re.sub(re.escape(background_phrase), " ", working, flags=re.IGNORECASE)

    for noise_pattern in SIGNATURE_NOISE_PATTERNS:
        working = re.sub(noise_pattern, " ", working, flags=re.IGNORECASE)

    working = normalize_prompt_text(working).strip(" ,.;:-")
    if not working:
        return None, ""

    hints: list[str] = []
    lowered = working.lower()
    for keywords, english_hint in SIGNATURE_STYLE_KEYWORDS:
        if any(keyword in lowered for keyword in keywords):
            hints.append(english_hint)

    if not hints:
        translated = translate_for_description(working)
        if translated and translated != working:
            hints.append(translated)

    deduped_hints = list(dict.fromkeys(hints))
    return working, ", ".join(deduped_hints)


def build_ai_prompt(prompt: str, section: str, original_prompt: str = "") -> str:
    return compose_generation_debug(prompt, section, original_prompt)["final_prompt"]


def compose_generation_debug(prompt: str, section: str, original_prompt: str = "") -> dict:
    section_name = normalize_section(section)
    normalized_original = normalize_prompt_text(original_prompt or prompt)
    width, height = get_generation_dimensions(section_name)

    sanitized_prompt = sanitize_prompt(normalized_original)
    debug = {
        "section": section_name,
        "original_prompt": normalized_original,
        "sanitized_prompt": sanitized_prompt,
        "provider": "pollinations",
        "model": "flux",
        "width": width,
        "height": height,
    }

    if section_name == "signature":
        display_name, remainder = extract_signature_name(normalized_original)
        background_hint, background_prompt, ink_prompt, keep_background, background_phrase = detect_signature_background(normalized_original)
        style_source, style_hint = build_signature_style_hint(remainder, display_name, background_phrase)
        is_arabic_request = wants_arabic_script(prompt, normalized_original)

        arabic_calligraphy_instruction = ""
        if contains_arabic(display_name) or is_arabic_request:
            arabic_calligraphy_instruction = (
                f"The name MUST be written in Arabic calligraphy letterforms. "
                f"Use the exact Arabic text: '{display_name}'. "
                "Do NOT transliterate into Latin/English letters. "
                "Render Arabic script flowing right-to-left with authentic ink strokes. "
            )

        style_sentence = f"Style cues: {style_hint}. " if style_hint else ""
        final_prompt = (
            f"Professional handwritten signature for '{display_name}', "
            "single flowing cursive calligraphy, authentic ink pen signature style, "
            f"{background_prompt}, {ink_prompt}, fine detailed strokes, "
            f"{style_sentence}"
            f"{arabic_calligraphy_instruction}"
            "no portrait, no face, no person, no mascot, no badge, no emblem, "
            "no seal, no icon, no logo mark, no frame, no scenery, no watermark"
        )

        debug.update({
            "display_name": display_name,
            "wants_arabic_script": is_arabic_request,
            "style_hint": style_source or None,
            "background_hint": background_hint,
            "background_conflict": keep_background,
            "final_prompt": final_prompt,
        })
        return debug

    if section_name == "icon":
        subject_source = sanitized_prompt or "app"
        english_subject = translate_for_description(subject_source)
        final_prompt = (
            f"Professional app icon design for {english_subject}, centered symbol, bold simple silhouette, "
            "clean vector style, strong contrast, polished modern icon, isolated on white background, "
            "no text, no letters, no words, no watermark"
        )
        debug.update({
            "subject_source": subject_source,
            "translated_subject": english_subject,
            "final_prompt": final_prompt,
        })
        return debug

    subject_source = sanitized_prompt or "brand"
    english_subject = translate_for_description(subject_source)
    final_prompt = (
        f"Professional high-quality logo design of {english_subject}, stunning details, vivid colors, "
        "vector graphic style illustration, elegant masterpiece, isolated on white background, "
        "no text, no watermark"
    )
    debug.update({
        "subject_source": subject_source,
        "translated_subject": english_subject,
        "final_prompt": final_prompt,
    })
    return debug


def ensure_rembg_loaded() -> None:
    global remove, new_session
    if remove is not None and new_session is not None:
        return
    try:
        from rembg import remove as rembg_remove, new_session as rembg_new_session

        remove = rembg_remove
        new_session = rembg_new_session
    except ImportError as error:
        print(f"Error importing imaging libraries: {error}. Ensure rembg and pillow are installed.")
        remove = None
        new_session = None


def get_rembg_session():
    global rembg_session
    ensure_rembg_loaded()
    if rembg_session is not None or new_session is None:
        return rembg_session
    with rembg_session_lock:
        if rembg_session is None:
            rembg_session = new_session("u2netp")
    return rembg_session


@router.post("/generate-logo", response_model=LogoGenerationResponse)
def generate_logo(req: LogoRequest):
    try:
        section = normalize_section(req.section)
        debug = compose_generation_debug(req.prompt, section, req.prompt)
        ai_prompt = debug["final_prompt"]
        width = debug["width"]
        height = debug["height"]
        seed = req.seed if req.seed else random.randint(1, 1_000_000_000)

        url = (
            "https://image.pollinations.ai/prompt/"
            f"{requests.utils.quote(ai_prompt)}?width={width}&height={height}"
            f"&nologo=true&enhance=true&model=flux&seed={seed}"
        )

        explicit_background_requested = bool(debug.get("background_hint")) and debug.get("background_hint") != "transparent"
        effective_remove_background = req.remove_background and not explicit_background_requested

        response_debug = LogoGenerationDebug(
            **debug,
            seed=seed,
            remove_background=req.remove_background,
            effective_remove_background=effective_remove_background,
            background_conflict=bool(req.remove_background and explicit_background_requested),
            generator_url=url,
        )

        print(f"[AI] Section: {section} | Prompt: {ai_prompt}")
        response = requests.get(url, timeout=120)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to reach AI image generation service.")

        image_bytes = response.content

        if effective_remove_background:
            print("Removing background from AI generated image...")
            try:
                ensure_rembg_loaded()
                if remove is None:
                    raise RuntimeError("Background removal dependencies are not available.")
                session = get_rembg_session()
                image_bytes = remove(image_bytes, session=session) if session else remove(image_bytes)
                print("Background removed successfully.")
            except Exception as error:
                print(f"Background removal failed: {error}, returning original image.")

        base64_img = base64.b64encode(image_bytes).decode("utf-8")
        return LogoGenerationResponse(
            image_data=f"data:image/png;base64,{base64_img}",
            seed=seed,
            debug=response_debug,
        )
    except Exception as error:
        print(f"Error in API: {error}")
        raise HTTPException(status_code=500, detail=str(error))
