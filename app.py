from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import JSONResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import shutil
import traceback

app = FastAPI()

templates = Jinja2Templates(directory="templates")

BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        print("=== upload started ===")
        print("filename:", file.filename)
        print("content_type:", file.content_type)

        if not file.filename:
            return JSONResponse(
                status_code=400,
                content={"error": "Файл не передан"}
            )

        save_path = UPLOAD_DIR / file.filename
        print("save_path:", save_path)

        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        print("=== file saved ===")

        return JSONResponse(
            status_code=200,
            content={
                "status": "ok",
                "filename": file.filename,
                "path": str(save_path)
            }
        )

    except Exception as e:
        print("=== ERROR IN /upload ===")
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={
                "error": str(e),
                "type": e.__class__.__name__
            }
        )
