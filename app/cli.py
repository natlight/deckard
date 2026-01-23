import asyncio
import argparse
import sys
from app.ingest import process_text
import os

# Ensure we can import app modules
sys.path.append(os.getcwd())

async def main(text_input: str):
    print(f"Processing: {text_input}...")
    try:
        result = await process_text(text_input)
        print("\n--- Processed Note ---")
        print(f"Title: {result['note']['title']}")
        print(f"Category: {result['note']['category']}")
        print(f"Subcategory: {result['note']['subcategory']}")
        print(f"Saved to: {result['file_path']}")
        print("----------------------")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Deckard CLI")
    parser.add_argument("text", help="Text to process")
    args = parser.parse_args()
    
    asyncio.run(main(args.text))
