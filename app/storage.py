import os
import yaml
from datetime import datetime
from pathlib import Path
from app.models import ProcessedNote

DATA_DIR = Path("data")

def save_note(note: ProcessedNote) -> str:
    """
    Saves the processed note to the filesystem in an Obsidian-compatible format.
    Returns the absolute path of the saved file.
    """
    # Construct directory path: /data/{Category}/{Subcategory}
    # Sanitize category/subcategory for filesystem (basic)
    category_dir = DATA_DIR / note.category.value
    subcategory_dir = category_dir / note.subcategory.replace(" ", "_")
    
    # Ensure directories exist
    subcategory_dir.mkdir(parents=True, exist_ok=True)
    
    # Construct filename
    filename = note.suggested_filename
    if not filename.endswith(".md"):
        filename += ".md"
    
    file_path = subcategory_dir / filename
    
    # Prepare Frontmatter
    frontmatter = {
        "title": note.title,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tags": note.tags,
        "category": note.category.value,
        "subcategory": note.subcategory
    }
    
    # Write file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("---\n")
        yaml.dump(frontmatter, f, default_flow_style=False)
        f.write("---\n\n")
        f.write(f"# {note.title}\n\n")
        f.write(f"> {note.summary}\n\n")
        f.write(note.content)
        
    # Git Commit and Push
    try:
        # Check if we are in a git repo
        if (Path(os.getcwd()) / ".git").exists():
            import subprocess
            
            # Helper to run command
            def run_git(args):
                subprocess.run(["git"] + args, check=True, capture_output=True)
            
            # Setup git config if needed (or rely on env/docker config)
            # run_git(["config", "user.name", "Deckard Bot"]) 
            # run_git(["config", "user.email", "deckard@ai"])
            
            run_git(["add", str(file_path)])
            run_git(["commit", "-m", f"Add note: {note.title}"])
            run_git(["push"])
            print(f"Synced {filename} to GitHub.")
            
    except Exception as e:
        print(f"Git sync failed: {e}")
    
    return str(file_path)
