import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import base64

try:
    from rembg import remove, new_session
    from PIL import Image
    import io
    # Use lightweight model to prevent out-of-memory errors on free cloud tiers
    rembg_session = new_session("u2netp")
except ImportError as e:
    rembg_session = None
    print(f"Error importing imaging libraries: {e}. Ensure rembg and pillow are installed.")

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("deep-translator not found. Arabic translation will be skipped.")

app = FastAPI(title="Iconora Studio AI Engine")

# Allow the React frontend to communicate with this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LogoRequest(BaseModel):
    prompt: str
    remove_background: bool = True

def translate_to_english(text: str) -> str:
    """Translates Arabic text to English to improve AI generation accuracy."""
    try:
        # Check if the text contains arabic characters
        if any("\u0600" <= c <= "\u06FF" for c in text):
            translator = GoogleTranslator(source='auto', target='en')
            translated = translator.translate(text)
            print(f"Translated '{text}' to '{translated}' for AI generation")
            return translated
        return text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

@app.post("/api/generate-logo")
def generate_logo(req: LogoRequest):
    try:
        # 1. Translate Arabic prompt to English if needed
        english_prompt = translate_to_english(req.prompt)

        # 2. Add prompt engineering so the AI draws a clean logo, not a photo
        # Refined to prevent gibberish text. The user should add text using the canvas.
        filtered_prompt = english_prompt.replace("Design a logo for", "").replace("design a logo for", "").strip()
        ai_prompt = f"minimalist professional flat vector icon of [{filtered_prompt}], purely symbolic graphic, NO TEXT, textless, NO LETTERS, no typography, white background, clean lines, flat design masterpiece, isolated"
        
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
                if rembg_session:
                    image_bytes = remove(image_bytes, session=rembg_session)
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

if __name__ == "__main__":
    import uvicorn
    print("Starting Iconora AI Backend on http://127.0.0.1:8000")
    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
