import asyncio
import os
import sys

# Ensure we can import app modules
sys.path.append(os.getcwd())

from app.agent import agent

# Simulating the context from the user test request
TEST_INPUT = "process this link as a new project with the name of the llm used appended to the title. https://hevodata.com/learn/airflow-vs-azure-data-factory-comparison/"

async def run_test():
    provider = os.getenv('LLM_PROVIDER', 'unknown')
    print(f"Testing with provider: {provider}")
    print(f"Input: {TEST_INPUT}")
    try:
        # Run the agent
        # Note: agent.run() returns a RunResult which has .data for typed responses or .output for string?
        # App/agent.py defines output_type=ProcessedNote so it should be .data
        result = await agent.run(TEST_INPUT)
        
        print("\n--- Result ---")
        if hasattr(result, 'data'):
             print(f"Title: {result.data.title}")
             print(f"Category: {result.data.category}")
             print(f"Subcategory: {result.data.subcategory}")
             print(f"Summary: {result.data.summary}")
             print(f"Filename: {result.data.suggested_filename}")
        else:
             print(f"Raw Output: {result}")
             
    except Exception as e:
        print(f"Test Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_test())
