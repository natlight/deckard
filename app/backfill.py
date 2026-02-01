import os
import yaml
import logging
from pathlib import Path
from app.models import ProcessedNote, NoteCategory
from app.graph import graph

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "deckard-vault"

def parse_note_file(file_path: Path) -> ProcessedNote | None:
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Split by frontmatter delimiters
        parts = content.split('---')
        if len(parts) < 3:
            logger.warning(f"Skipping {file_path.name}: Invalid format (no frontmatter detected)")
            return None
            
        # Parse Frontmatter
        frontmatter = yaml.safe_load(parts[1])
        body = parts[2].strip()
        
        # Extract Summary and Content from Body
        # Format usually:
        # # Title
        # 
        # > Summary
        # 
        # Content...
        
        lines = body.split('\n')
        summary = ""
        actual_content_lines = []
        
        for line in lines:
            line = line.strip()
            if line.startswith("# "): 
                continue # Skip title repetition
            if line.startswith("> ") and not summary:
                summary = line[2:].strip()
                continue
            if not line and not actual_content_lines:
                continue # Skip leading empty lines
            actual_content_lines.append(line)
            
        actual_content = "\n".join(actual_content_lines)
        
        if not summary:
            summary = "No summary available."

        # Map to Pydantic Model
        return ProcessedNote(
            title=frontmatter.get('title', file_path.stem),
            category=NoteCategory(frontmatter.get('category', 'Resources')),
            subcategory=frontmatter.get('subcategory', 'General'),
            tags=frontmatter.get('tags', []),
            summary=summary,
            content=actual_content,
            suggested_filename=file_path.name
        )
        
    except Exception as e:
        logger.error(f"Failed to parse {file_path.name}: {e}")
        return None

def backfill() -> dict:
    logger.info("Starting Backfill Process...")
    
    # Ensure graph connection
    graph.connect()
    
    count = 0
    errors = 0
    # Walk through DATA_DIR
    for root, dirs, files in os.walk(DATA_DIR):
        for file in files:
            if file.endswith(".md"):
                file_path = Path(root) / file
                logger.info(f"Processing {file_path.name}...")
                
                note = parse_note_file(file_path)
                if note:
                    try:
                        graph.ingest_note(note, str(file_path))
                        count += 1
                    except Exception as e:
                        logger.error(f"Failed to ingest {file_path.name} into graph: {e}")
                        errors += 1
                else:
                    errors += 1
                    
    logger.info(f"Backfill Complete. Ingested {count} notes. Errors: {errors}")
    return {"ingested": count, "errors": errors}

if __name__ == "__main__":
    backfill()
