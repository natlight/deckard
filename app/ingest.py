from app.agent import agent, model_name
from app.models import ProcessedNote
from app.storage import save_note
from pydantic_ai import BinaryContent
from openai import AsyncOpenAI
import os
import aiofiles

async def process_text(text: str) -> dict:
    """
    Process raw text input using the PydanticAI agent and save the result.
    """
    result = await agent.run(text)
    note: ProcessedNote = result.output
    file_path = save_note(note)
    return {
        "status": "success",
        "file_path": file_path,
        "note": note.model_dump()
    }

async def process_image(image_data: bytes, media_type: str, context_text: str = "Analyze this image and organize it.") -> dict:
    """
    Process an image using PydanticAI's multimodal capabilities.
    """
    content = [
        context_text,
        BinaryContent(data=image_data, media_type=media_type)
    ]
    
    result = await agent.run(content)
    note: ProcessedNote = result.output
    file_path = save_note(note)
    
    return {
        "status": "success",
        "file_path": file_path,
        "note": note.model_dump()
    }

async def process_audio(audio_path: str) -> dict:
    """
    Transcribe audio using OpenAI Whisper then process the text.
    """
    # Initialize OpenAI client for Whisper (using same env vars)
    # Note: openrouter might support whisper, or use direct OpenAI or another provider.
    # We will assume OPENAI_API_KEY is set and compatible, or specifically configured.
    # If using OpenRouter, check if it supports audio/feature specific endpoints.
    # For now, we assume utilizing the configured base_url/key might work or fallback to default if user has keys.
    
    # Check if we need specific base_url for audio. OpenRouter often proxies LLMs, but audio might differ.
    # Using default client behavior which picks up OPENAI_API_KEY.
    
    client = AsyncOpenAI(
        base_url=os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1"),
        api_key=os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    )
    
    try:
        with open(audio_path, "rb") as audio_file:
            # Note: valid model for whisper on openrouter or openai
            # OpenRouter: 'openai/whisper' or similar? Defaults to 'whisper-1' for OpenAI.
            transcription = await client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file
            )
        
        text = transcription.text
        # Process the transcribed text
        return await process_text(text)
        
    except Exception as e:
        # Fallback for debugging - if transcription fails, maybe just log it
        raise e
