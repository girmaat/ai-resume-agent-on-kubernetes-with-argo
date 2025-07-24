from app.assistant.config.non_ai import config
from importlib import import_module

try:
    # Dynamically import tools for the current profile
    profile_module = import_module(f"app.assistant.config.tools.gi_{config.CURRENT_PROFILE}")
    TOOLS = profile_module.TOOLS
except ImportError as e:
    raise ImportError(
        f"Could not load tools for profile '{config.CURRENT_PROFILE}'. "
        f"Ensure tools/gi_{config.CURRENT_PROFILE}.py exists and contains TOOLS list"
    ) from e

__all__ = ['TOOLS']  # Explicit exports
