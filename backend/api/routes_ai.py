import base64
from threading import Lock

from fastapi import APIRouter, HTTPException
import requests

from backend.schemas.ai_models import LogoRequest

router = APIRouter()
rembg_session = None
rembg_session_lock = Lock()
remove = None
new_session = None

def ensure_rembg_loaded() -> None:
    global remove, new_session
    if remove is not None and new_session is not None:
        return
    try:
        from rembg import remove as rembg_remove, new_session as rembg_new_session

        remove = rembg_remove
        new_session = rembg_new_session
    except ImportError as e:
        print(f"Error importing imaging libraries: {e}. Ensure rembg and pillow are installed.")
        remove = None
        new_session = None


def get_rembg_session():
    global rembg_session
    ensure_rembg_loaded()
    if rembg_session is not None or new_session is None:
        return rembg_session
    with rembg_session_lock:
        if rembg_session is None:
            # Delay model loading until the feature is actually used.
            rembg_session = new_session("u2netp")
    return rembg_session

def translate_to_english(text: str) -> str:
    """Translates Arabic text to English to improve AI generation accuracy."""
    try:
        # Check if the text contains arabic characters
        if any("\u0600" <= c <= "\u06FF" for c in text):
            try:
                from deep_translator import GoogleTranslator
                translator = GoogleTranslator(source='auto', target='en')
                translated = translator.translate(text)
                print(f"Translated '{text}' to '{translated}' for AI generation")
                return translated
            except ImportError:
                print("deep-translator not found. Arabic translation will be skipped.")
                return text
        return text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

@router.post("/generate-logo")
def generate_logo(req: LogoRequest):
    try:
        # 1. Translate Arabic prompt to English if needed
        english_prompt = translate_to_english(req.prompt)

        # 2. Add prompt engineering so the AI draws a clean logo, not a photo
        filtered_prompt = english_prompt.replace("Design a logo for", "").replace("design a logo for", "").strip()
        # Truncate to avoid URL length limit errors if the user writes a very long prompt
        if len(filtered_prompt) > 300:
            filtered_prompt = filtered_prompt[:300]
            
        ai_prompt = f"Professional high-quality logo design of {filtered_prompt}, stunning details, vivid colors, vector graphic style illustration, elegant masterpiece, isolated on white background, NO TEXT, textless"
        
        import random
        seed = random.randint(1, 1000000)
        # 3. Request Image from a free community API (Pollinations uses Stable Diffusion / Midjourney like models)
        print(f"Generating image for prompt: {ai_prompt}")
        url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(ai_prompt)}?width=512&height=512&nologo=true&model=flux&seed={seed}"
        
        response = requests.get(url, timeout=120)
        if response.status_code != 200:
            raise HTTPException(status_code=500, detail="Failed to reach AI image generation service.")

        image_bytes = response.content

        # 4. Remove the Background using rembg (making the logo transparent!)
        if req.remove_background:
            print("Removing background from AI generated image...")
            try:
                # rembg expects bytes and returns bytes containing a PNG with alpha channel
                ensure_rembg_loaded()
                if remove is None:
                    raise RuntimeError("Background removal dependencies are not available.")
                session = get_rembg_session()
                if session:
                    image_bytes = remove(image_bytes, session=session)
                else:
                    image_bytes = remove(image_bytes)
                print("Background removed successfully.")
            except Exception as e:
                print(f"Background removal failed: {e}, returning original image.")

        # 5. Convert to Base64 to send to React Front-end
        base64_img = base64.b64encode(image_bytes).decode('utf-8')
        
        return {"image_data": f"data:image/png;base64,{base64_img}"}

    except Exception as e:
        print(f"Error in API: {e}")
        raise HTTPException(status_code=500, detail=str(e))
