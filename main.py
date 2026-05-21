from pathlib import Path
import shutil
import traceback
import uuid

from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from app.services.pipeline import run_pipeline

app = FastAPI()

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


@app.post("/upload")
async def upload_video(
    file: UploadFile = File(...),
    target_level: str = Form("A2-B1")
):
    try:
        file_id = str(uuid.uuid4())
        ext = Path(file.filename).suffix if file.filename else ".mp4"
        saved_path = UPLOAD_DIR / f"{file_id}{ext}"

        with saved_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = run_pipeline(str(saved_path), target_level=target_level)

        return JSONResponse({
            "message": "Видео успешно обработано",
            "file_id": file_id,
            "saved_video_path": str(saved_path),
            "result": result
        })

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "traceback": traceback.format_exc()
            }
        )