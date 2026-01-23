from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field

class NoteCategory(str, Enum):
    PROJECTS = "Projects"
    AREAS = "Areas"
    RESOURCES = "Resources"
    ARCHIVES = "Archives"

class ProcessedNote(BaseModel):
    """
    Structured output for a processed note, classified into the PARA method.
    """
    title: str = Field(..., description="A concise and descriptive title for the note.")
    category: NoteCategory = Field(..., description="The PARA category (Projects, Areas, Resources, Archives).")
    subcategory: str = Field(..., description="The specific subcategory or project name (e.g., 'Home Renovation', 'Health', 'Python Learning').")
    tags: List[str] = Field(..., description="List of relevant tags for the note.")
    summary: str = Field(..., description="A brief summary of the content.")
    content: str = Field(..., description="The processed markdown content of the note.")
    suggested_filename: str = Field(..., description="A unique and filesystem-safe filename for the note (ending in .md).")
