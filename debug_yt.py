from youtube_transcript_api import YouTubeTranscriptApi
import sys

import inspect
try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch("jNQXAC9IVRw")
    print(f"Transcript length: {len(transcript)}")
    print(transcript[:2])
except Exception as e:
    print(f"Error: {e}")
