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
    parser.add_argument("text", nargs="?", help="Text to process")
    parser.add_argument("--backfill", action="store_true", help="Backfill Knowledge Graph from existing notes")
    parser.add_argument("--clear-graph", action="store_true", help="Delete all data in Knowledge Graph")
    
    args = parser.parse_args()
    
    if args.clear_graph:
        from app.graph import graph
        print("WARNING: This will delete all data in the Knowledge Graph.")
        confirm = input("Are you sure? (y/N): ")
        if confirm.lower() == 'y':
            if graph.clear_database():
                print("Graph cleared successfully.")
            else:
                print("Failed to clear graph.")
        else:
            print("Operation cancelled.")
            
    elif args.backfill:
        from app.backfill import backfill
        print("Starting backfill...")
        stats = backfill()
        print(f"Backfill complete: {stats}")
    elif args.text:
        asyncio.run(main(args.text))
    else:
        parser.print_help()
