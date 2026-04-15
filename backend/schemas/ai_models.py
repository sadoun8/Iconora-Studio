from pydantic import BaseModel


class LogoRequest(BaseModel):
    prompt: str
    remove_background: bool = True
    seed: int | None = None
    section: str = "logo"


class LogoGenerationDebug(BaseModel):
    section: str
    original_prompt: str
    sanitized_prompt: str
    final_prompt: str
    subject_source: str | None = None
    translated_subject: str | None = None
    display_name: str | None = None
    wants_arabic_script: bool | None = None
    style_hint: str | None = None
    background_hint: str | None = None
    background_conflict: bool | None = None
    provider: str = "pollinations"
    model: str = "flux"
    width: int
    height: int
    seed: int | None = None
    remove_background: bool = True
    effective_remove_background: bool | None = None
    generator_url: str | None = None


class LogoGenerationResponse(BaseModel):
    image_data: str
    seed: int | None = None
    debug: LogoGenerationDebug | None = None
