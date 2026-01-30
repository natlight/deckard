import os
import sys

# Mock environment
os.environ["LLM_PROVIDER"] = "openai"
os.environ["OPENAI_API_KEY"] = "sk-fake-key"
os.environ["OPENAI_MODEL"] = "gpt-4o"
os.environ["OPENAI_REASONING_EFFORT"] = "medium"

try:
    from app.agent import agent, model_settings
    print(f"Agent initialized.")
    if model_settings:
        print(f"Model settings: {model_settings}")
        # Check internal dict if possible
        if hasattr(model_settings, 'openai_reasoning_effort'):
            print(f"Reasoning effort: {model_settings.openai_reasoning_effort}")
    else:
        print("Model settings is None")

except Exception as e:
    print(f"Error during import/init: {e}")
