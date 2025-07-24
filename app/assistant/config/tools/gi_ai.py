from app.assistant.config.tools.base_tools import SHARED_TOOLS

AI_SPECIFIC_TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "debug_llm_prompt",
            "description": "Analyze and optimize an LLM prompt for better performance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "prompt": {"type": "string", "description": "The prompt to debug"},
                    "context": {"type": "string", "description": "Additional context (e.g., model used)"}
                },
                "required": ["prompt"]
            }
        }
    }
]

TOOLS = SHARED_TOOLS + AI_SPECIFIC_TOOLS  # Combine shared and AI-specific tools
