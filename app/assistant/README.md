# Assistant Configuration

This directory contains all configuration files for the AI assistant.

## Files

### `prompts.py`
- Contains all system prompt templates
- Uses Python f-strings for dynamic content
- Includes:
  - Base assistant identity prompt
  - Tool usage instructions
  - Content section templates

### `tools.py`
- Defines all available tools for the assistant
- Follows OpenAI's tool specification format
- Current tools:
  - `record_user_details`: Collects contact information
  - `record_unknown_query`: Logs unanswerable questions

### `non_ai.py`
- Contains non-AI related configurations
- Includes paths to static resources
- Defines UI constants and settings

### Usage
Import configurations directly in your assistant:
```python
from app.assistant.config.prompts import get_system_prompt
from app.assistant.config.tools import TOOLS
