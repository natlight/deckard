import asyncio
import os
from app.agent import agent

# Mock env setup if needed (agent import handles it via logic added earlier)

async def debug():
    print("Running agent...")
    try:
        # We need to set the env var for the agent to initialize correctly if not already (it is handled in agent.py)
        # But we need to ensure the key is there for the run.
        if "OPENAI_API_KEY" not in os.environ:
             # Try to source from OPENROUTER_API_KEY if present
             if "OPENROUTER_API_KEY" in os.environ:
                 os.environ["OPENAI_API_KEY"] = os.environ["OPENROUTER_API_KEY"]
                 
        result = await agent.run("Test debug note")
        print("\n--- Result Object ---")
        print(f"Type: {type(result)}")
        print(f"Dir: {dir(result)}")
        try:
            print(f"Data: {result.data}")
        except Exception as e:
            print(f"No .data: {e}")
            
        try:
            print(f"Output: {result.output}")
        except Exception as e:
            print(f"No .output: {e}")
            
    except Exception as e:
        print(f"Agent Run Failed: {e}")

if __name__ == "__main__":
    asyncio.run(debug())
