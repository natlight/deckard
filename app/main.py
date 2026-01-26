from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ingest import process_text, process_image, process_audio
import uvicorn
import shutil
import os
import tempfile

app = FastAPI(title="Deckard", description="AI-powered Second Brain", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class TextIngestRequest(BaseModel):
    text: str

@app.post("/api/ingest/text")
async def ingest_text(request: TextIngestRequest):
    try:
        result = await process_text(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest/image")
async def ingest_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        media_type = file.content_type
        result = await process_image(contents, media_type)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/ingest/audio")
async def ingest_audio(file: UploadFile = File(...)):
    try:
        # Save to temp file for ffmpeg/openai client usage
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name
        
        try:
            result = await process_audio(tmp_path)
            return result
        finally:
            os.remove(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static files at root (must be last to avoid masking API routes)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
