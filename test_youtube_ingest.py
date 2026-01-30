import asyncio
import os
from app.ingest import process_text

# Mock env if needed (same as debug_agent)
if "OPENAI_API_KEY" not in os.environ:
     if "OPENROUTER_API_KEY" in os.environ:
         os.environ["OPENAI_API_KEY"] = os.environ["OPENROUTER_API_KEY"]

async def test_youtube():
    # A short video: "Me at the zoo" or similar, or a technical one
    # Let's use a very short one to avoid huge context, e.g. "Me at the zoo" (ID: jNQXAC9IVRw)
    url = "https://www.youtube.com/watch?v=jNQXAC9IVRw" 
    print(f"Testing URL: {url}")
    
    try:
        result = await process_text(url)
        print("\n--- Result ---")
        print(f"Status: {result['status']}")
        print(f"File Path: {result['file_path']}")
        print("Note Content Snippet:")
        # We know note is a dict here because process_text returns dict
        print(result['note']['content'][:500]) 
    except Exception as e:
        print(f"Test Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_youtube())
