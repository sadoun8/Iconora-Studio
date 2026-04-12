from typing import Any

from pydantic import BaseModel, Field


class ExportCanvasRequest(BaseModel):
    format: str = Field(pattern="^(png|webp|pdf|ico|svg)$")
    section: str = "logo"
    width: int
    height: int
    transparent: bool = False
    canvas: dict[str, Any] | None = None
    data_url: str | None = None
    svg_text: str | None = None
    output_preset: str | None = None
    filename: str | None = None


class ExportIconPackRequest(BaseModel):
    width: int
    height: int
    canvas: dict[str, Any] | None = None
    data_url: str
    filename: str | None = None


class ExportResponse(BaseModel):
    success: bool
    message: str
    output_path: str | None = None
    warnings: list[str] = Field(default_factory=list)
