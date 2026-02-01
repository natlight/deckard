from app.agent import agent, model_name
from app.models import ProcessedNote
from app.storage import save_note
from pydantic_ai import BinaryContent
from openai import AsyncOpenAI
import os
import aiofiles
import logging

import re
from youtube_transcript_api import YouTubeTranscriptApi

logger = logging.getLogger(__name__)

def extract_video_id(url: str) -> str | None:
    """
    Extracts the video ID from a YouTube URL.
    Supports youtube.com and youtu.be.
    """
    # Regex for standard youtube.com and youtu.be URLs
    # Matches: ?v=ID, &v=ID, /v/ID, /embed/ID, /ID (short), etc.
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.search(regex, url)
    if match:
        return match.group(1)
    return None

def get_transcript(video_id: str) -> str | None:
    """
    Fetches the transcript for a given YouTube video ID.
    Returns the transcript as a single string or None if failed.
    """
    try:
        # Instantiate the API (v1.2.3+)
        yt = YouTubeTranscriptApi()
        # Returns a list of FetchedTranscriptSnippet objects (or similar)
        transcript_list = yt.fetch(video_id)
        
        # Combine valid text parts using object attribute .text
        full_text = " ".join([item.text for item in transcript_list])
        return full_text
    except Exception as e:
        logger.warning(f"Failed to get transcript for {video_id}: {e}")
        return None

async def process_text(text: str) -> dict:
    """
    Process raw text input using the PydanticAI agent and save the result.
    If a YouTube URL is found, attempts to fetch and append the transcript.
    """
    # Check for YouTube URL
    video_id = extract_video_id(text)
    
    if video_id:
        logger.info(f"Detected YouTube Video ID: {video_id}")
        transcript = get_transcript(video_id)
        if transcript:
            logger.info(f"Fetched transcript ({len(transcript)} chars)")
            text += f"\n\n--- YOUTUBE TRANSCRIPT ---\n\n{transcript}\n\n--- END TRANSCRIPT ---"
            
    result = await agent.run(text)
    note: ProcessedNote = result.output
    file_path = save_note(note)
    logger.info(f"Successfully processed text -> {file_path}")
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
    
    logger.info(f"Successfully processed image -> {file_path}")
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
        logger.info(f"Audio transcription complete: {len(text)} chars")
        # Process the transcribed text
        return await process_text(text)
        
    except Exception as e:
        # Fallback for debugging - if transcription fails, maybe just log it
        logger.error(f"Audio processing failed: {e}")
        raise e
