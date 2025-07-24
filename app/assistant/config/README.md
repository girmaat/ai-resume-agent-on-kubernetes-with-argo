# Assistant Configuration Module

This directory contains all configuration files for the AI Resume Assistant. The files are organized to separate different types of configurations for better maintainability.

## File Structure

config/
├── prompts.py # All prompt templates and instructions
├── tools.py # Tool definitions for function calling
├── non_ai.py # Non-AI related configurations
└── README.md # This documentation


## 1. prompts.py

Contains all system prompts and message templates used by the assistant.

### Example Contents:
```python
from app.assistant.config import config

def get_base_prompt() -> str:
    """Returns the core identity prompt for the assistant"""
    return f"""
You are acting as {config.PERSONAL['name']}, a professional {config.PERSONAL['title']}.

Your job is to answer questions about {config.PERSONAL['name']}'s experience, 
skills, background, and projects using the provided context.
"""

def get_tool_instructions() -> str:
    """Instructions for when to use available tools"""
    return """
If a user expresses interest (e.g., wants to follow up or collaborate):
- Use the 'record_user_details' tool to collect their contact information

If a question cannot be answered confidently:
- Use the 'record_unknown_query' tool to log the question
"""

def get_system_prompt(summary: str, resume: str) -> str:
    """Assembles the complete system prompt"""
    return (
        get_base_prompt() + 
        get_tool_instructions() +
        f"\n\n## Professional Summary:\n{summary}" +
        f"\n\n## Resume Content:\n{resume}"
    )

## 2. tools.py

Defines all tools available for the assistant's function calling capability.
Example Contents:

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "record_user_details",
            "description": "Collect contact information from interested users",
            "parameters": {
                "type": "object",
                "properties": {
                    "email": {
                        "type": "string",
                        "description": "The user's email address"
                    },
                    "name": {
                        "type": "string",
                        "description": "User's full name",
                        "default": "Not provided"
                    },
                    "notes": {
                        "type": "string",
                        "description": "Additional user comments",
                        "default": "None"
                    }
                },
                "required": ["email"]
            }
        }
    },
    # Additional tools...
]

# 3. non_ai.py

Contains configurations not directly related to AI operations.

