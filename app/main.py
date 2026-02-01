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

# Static mount moved to end to avoid shadowing API routes

# --- OpenAI Compatible API ---
from app.agent import chat_agent
from pydantic_ai.messages import ModelMessage, ModelRequest, ModelResponse, TextPart, UserPromptPart
import uuid
import time

# Simple in-memory session store is less relevant for OpenAI API which is stateless per request mostly,
# but Open WebUI sends full history each time usually.
# So we can just reconstruct history from the 'messages' payload.

class OpenAIMessage(BaseModel):
    role: str
    content: str

class ChatCompletionRequest(BaseModel):
    model: str
    messages: list[OpenAIMessage]
    stream: bool = False

@app.get("/v1/models")
async def list_models():
    return {
        "object": "list",
        "data": [
            {
                "id": "deckard",
                "object": "model",
                "created": int(time.time()),
                "owned_by": "deckard-ai"
            }
        ]
    }

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    # 1. Convert OpenAI messages to PydanticAI history
    # The last message is the new user prompt
    if not request.messages:
        raise HTTPException(status_code=400, detail="No messages provided")
    
    new_msg_content = request.messages[-1].content
    
    # Convert previous messages to history
    # This is a basic conversion. For robust production usage, we'd map function calls etc.
    history: list[ModelMessage] = []
    for msg in request.messages[:-1]:
        if msg.role == "user":
            history.append(ModelRequest(parts=[UserPromptPart(content=msg.content)]))
        elif msg.role == "assistant":
            history.append(ModelResponse(parts=[TextPart(content=msg.content)]))
            
    try:
        # 2. Run Agent
        # We ignore 'stream' for now as planned
        result = await chat_agent.run(new_msg_content, message_history=history)
        
        # 3. Format Response as OpenAI
        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": request.model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": result.output
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0, # Placeholder
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

    except Exception as e:
        logger.error(f"Chat completion error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- Maintenance Endpoints ---
from fastapi import BackgroundTasks
from app.backfill import backfill

@app.post("/api/maintenance/backfill")
async def trigger_backfill(background_tasks: BackgroundTasks):
    """
    Triggers a background backfill of the Knowledge Graph from existing notes.
    """
    background_tasks.add_task(backfill)
    return {"status": "Backfill job started"}

from app.graph import graph

@app.post("/api/maintenance/clear-graph")
async def clear_graph():
    """
    Deletes all nodes and relationships in the Knowledge Graph.
    """
    success = graph.clear_database()
    if success:
        return {"status": "Knowledge Graph cleared"}
    else:
        raise HTTPException(status_code=500, detail="Failed to clear graph")

# Mount static files at root (must be last to avoid masking API routes)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
# Mount at root must be truly last
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
