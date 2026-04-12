from fastapi import APIRouter, HTTPException
from backend.schemas.export_models import (
    ExportCanvasRequest,
    ExportIconPackRequest,
    ExportResponse,
)
from backend.services.export_service import export_canvas, export_icon_pack

router = APIRouter()

@router.post("/canvas", response_model=ExportResponse)
def export_canvas_route(req: ExportCanvasRequest):
    try:
        output_path, warnings = export_canvas(
            data_url=req.data_url or "",
            export_format=req.format,
            filename=req.filename,
            svg_text=req.svg_text,
        )
        return ExportResponse(
            success=True,
            message=f"Exported successfully to {req.format}",
            output_path=output_path,
            warnings=warnings,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/icon-pack")
def export_icon_pack_route(req: ExportIconPackRequest):
    try:
        output_path, large_paths, warnings = export_icon_pack(
            data_url=req.data_url,
            filename=req.filename,
        )
        return {
            "success": True,
            "message": "Icon pack exported successfully",
            "output_path": output_path,
            "large_paths": large_paths,
            "warnings": warnings,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
