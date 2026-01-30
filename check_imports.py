try:
    from pydantic_ai.models.gemini import GeminiModel
    print("GeminiModel found in pydantic_ai.models.gemini")
except ImportError:
    print("GeminiModel NOT found in pydantic_ai.models.gemini")
    try:
        from pydantic_ai.models.google import GoogleModel
        print("GoogleModel found in pydantic_ai.models.google")
    except ImportError:
        print("GoogleModel NOT found")

try:
    from pydantic_ai.models.anthropic import AnthropicModel
    print("AnthropicModel found in pydantic_ai.models.anthropic")
except ImportError:
    print("AnthropicModel NOT found")
