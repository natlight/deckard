import os
from pydantic_ai import Agent
from app.models import ProcessedNote
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIModel
from openai import AsyncOpenAI

load_dotenv()

# Check for API keys
api_key = os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL", "https://openrouter.ai/api/v1")

if not api_key:
    print("WARNING: No API Key found. Agent may fail.")

# Correct OpenRouter Model ID
model_name = 'openai/gpt-5.2'

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
- If the input contains a **YouTube Transcript**, use it to analyze the video's content. Summarize the key points, extract insights, and treat the transcript as the primary source of information. The title should reflect the VIDEO content.

Be intelligent about where things go. If it's a actionable task, it's likely a Project (or part of one). If it's something to maintain (like Health or Finances), it's an Area. If it's reference material, it's a Resource.
"""

# Create a custom client with the correct base_url
client = AsyncOpenAI(
    api_key=api_key,
    base_url=base_url
)

# Initialize OpenAIModel with the custom client
# Note: PydanticAI v0.0.49+ uses 'openai_client' or similar param to pass explicit client?
# If 'openai_client' is not supported, we rely on the client utilizing system variables, 
# BUT we need to pass the client to the model to force base_url usage if env vars aren't picked up globally by 'openai' lib automatically inside the model.
# Let's try passing it as the 'openai_client' arg which is common in wrappers, or rely on explicit manual check.
# Actually, the safest way if we don't know the exact PydanticAI version arg name is to use the environment variables 
# which we just fixed in docker-compose.
# So we will revert to simple instantiation and rely on the now-present OPENAI_BASE_URL env var.

# FORCE OPENAI_API_KEY to be the resolved key, so OpenAIModel picks it up automatically
if api_key:
    os.environ["OPENAI_API_KEY"] = api_key

model = OpenAIModel(model_name)

agent = Agent(
    model=model,
    system_prompt=SYSTEM_PROMPT,
    output_type=ProcessedNote
)
