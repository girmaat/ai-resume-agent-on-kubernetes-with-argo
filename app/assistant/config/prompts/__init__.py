from app.assistant.config.non_ai import config
from importlib import import_module

try:
    profile_module = import_module(f"app.assistant.config.prompts.gi_{config.CURRENT_PROFILE}")
    get_system_prompt = profile_module.get_system_prompt
except ImportError as e:
    raise ImportError(
        f"Could not load prompts for profile '{config.CURRENT_PROFILE}'. "
        f"Ensure prompts/gi_{config.CURRENT_PROFILE}.py exists and contains get_system_prompt()"
    ) from e
