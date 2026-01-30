from pydantic_ai.models.openai import OpenAIModel
try:
    from pydantic_ai.models.openai import OpenAIModelSettings
    print("OpenAIModelSettings found")
except ImportError:
    print("OpenAIModelSettings NOT found")

import inspect
print(f"OpenAIModel init signature: {inspect.signature(OpenAIModel.__init__)}")
