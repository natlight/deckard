import logging
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.ingest import process_text, process_image, process_audio
import uvicorn
import shutil
import os
import tempfile

# Configure logging for the application if not already configured by imported modules
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

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
async def ingest_image(file: UploadFile = File(...), context_text: str = Form(None)):
    try:
        contents = await file.read()
        media_type = file.content_type
        if context_text:
            result = await process_image(contents, media_type, context_text)
        else:
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

# --- Chat Endpoint ---
from app.agent import chat_agent
from pydantic_ai.messages import ModelMessage
import uuid

# Simple in-memory session store: session_id -> list[ModelMessage]
sessions: dict[str, list[ModelMessage]] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None

@app.post("/api/chat")
async def chat_endpoint(request: ChatRequest):
    session_id = request.session_id or str(uuid.uuid4())
    
    # Retrieve history or start fresh
    history = sessions.get(session_id, [])
    
    try:
        # Run agent with history
        # PydanticAI manages history appending if we pass it correctly
        result = await chat_agent.run(request.message, message_history=history)
        
        # Update history with new messages (User + AI response)
        # result.new_messages() returns the messages added during this run
        sessions[session_id] = history + result.new_messages()
        
        return {
            "response": result.data,
            "session_id": session_id
        }
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
