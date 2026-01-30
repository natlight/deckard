import os
import sys
from pydantic_ai import Agent
from app.models import ProcessedNote
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.models.gemini import GeminiModel
from pydantic_ai.models.anthropic import AnthropicModel
from openai import AsyncOpenAI

load_dotenv()

# Configuration
# options: openrouter, openai, gemini, claude
llm_provider = os.getenv("LLM_PROVIDER", "openrouter").lower()

print(f"Initializing Deckard Agent with Provider: {llm_provider}")

model = None
model_settings = None

if llm_provider == "openrouter":
    # OpenRouter (uses OpenAI interface)
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = "https://openrouter.ai/api/v1"
    model_name = os.getenv("OPENROUTER_MODEL", "openai/gpt-5.2") 
    
    if not api_key:
        print("WARNING: No API Key found for OpenRouter.")
    
    # Set env vars for OpenAIModel to pick up
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_BASE_URL"] = base_url
    
    model = OpenAIModel(model_name)

elif llm_provider == "openai":
    # Direct OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    model_name = os.getenv("OPENAI_MODEL", "gpt-4o")
    reasoning_effort = os.getenv("OPENAI_REASONING_EFFORT")
    
    if not api_key:
        print("WARNING: No API Key found for OpenAI.")
    
    # Ensure env var is set
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
    if "OPENAI_BASE_URL" in os.environ and "openrouter" in os.environ["OPENAI_BASE_URL"]:
        # clear base url if it was set to openrouter previously in env
        del os.environ["OPENAI_BASE_URL"]
        
    model = OpenAIModel(model_name)
    
    if reasoning_effort:
        try:
            # Attempt to configure reasoning effort if supported
            from pydantic_ai.models.openai import OpenAIModelSettings
            # Note: Parameter name based on pydantic-ai docs for O1 support
            model_settings = OpenAIModelSettings(openai_reasoning_effort=reasoning_effort)
            print(f"Applied OpenAI reasoning effort: {reasoning_effort}")
        except Exception as e:
            print(f"WARNING: Could not apply reasoning effort: {e}")

elif llm_provider == "gemini":
    # Google Gemini
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    if not api_key:
        print("WARNING: No API Key found for Gemini.")
    
    if api_key:
        os.environ["GEMINI_API_KEY"] = api_key
        
    model = GeminiModel(model_name)

elif llm_provider == "claude":
    # Anthropic Claude
    api_key = os.getenv("ANTHROPIC_API_KEY")
    model_name = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-latest")
    
    if not api_key:
        print("WARNING: No API Key found for Claude.")
    
    if api_key:
        # PydanticAI usually looks for ANTHROPIC_API_KEY
        os.environ["ANTHROPIC_API_KEY"] = api_key
        
    model = AnthropicModel(model_name)

else:
    # Fallback or Error
    print(f"ERROR: Unknown LLM_PROVIDER '{llm_provider}'. Falling back to OpenRouter.")
    llm_provider = "openrouter"
    api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
    base_url = "https://openrouter.ai/api/v1"
    os.environ["OPENAI_BASE_URL"] = base_url
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        
    model = OpenAIModel('openai/gpt-5.2')

SYSTEM_PROMPT = """
You are Deckard, an advanced digital twin and "second brain" assistant. 
Your goal is to process incoming information (notes, ideas, tasks, resources) and organize them using the PARA method:

- **Projects**: A series of tasks linked to a goal, with a deadline.
- **Areas**: A sphere of activity with a standard to be maintained over time.
- **Resources**: A topic or theme of ongoing interest.
- **Archives**: Inactive items from the other three categories.

For each input:
1. Analyze the content.
2. Determine the most appropriate PARA category and a specific subcategory (e.g., Project Name or Area of Responsibility).
3. Generate a descriptive title and summary.
4. Extract relevant tags.
5. Format the content in **Obsidian-optimized Markdown**.
6. Suggest a filename.

**Formatting Rules for Content:**
- **Do NOT** include the Title or Summary at the top of the content body (these are added automatically by the system).
- ALL links to other concepts or potential notes must use **Wikilinks** format: `[[Concept Name]]`.
- Use **Callouts** for important info, warnings, or distinctive blocks: `> [!INFO] Title` or `> [!WARNING]`.
- Use standard Markdown headers (H2, H3) to structure the note (start with H2 as H1 is the title).
- Use bullet points and lists for readability.
- If the note is a Task/Project, use checkboxes `[ ]`.

**Special Instructions:**
- **Do NOT** output any markdown fencing like ```markdown or ``` around the entire response. Just the raw markdown content.
- If the input contains a **YouTube Transcript**, use it to analyze the video's content. Summarize the key points, extract insights, and treat the transcript as the primary source of information. The title should reflect the VIDEO content.

Be intelligent about where things go. If it's a actionable task, it's likely a Project (or part of one). If it's something to maintain (like Health or Finances), it's an Area. If it's reference material, it's a Resource.
"""

agent = Agent(
    model=model,
    model_settings=model_settings,
    system_prompt=SYSTEM_PROMPT,
    output_type=ProcessedNote
)
