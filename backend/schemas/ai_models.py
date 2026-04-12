from pydantic import BaseModel


class LogoRequest(BaseModel):
    prompt: str
    remove_background: bool = True


class LogoGenerationResponse(BaseModel):
    image_data: str
