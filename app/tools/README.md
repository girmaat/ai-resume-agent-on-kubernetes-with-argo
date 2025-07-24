# Tools Package

This package contains all tool implementations for the AI assistant.

## Structure

- `channels/`: Notification channel implementations
- `dispatcher.py`: Central tool dispatcher
- `log_unknown.py`: Unknown question logger
- `notify_user.py`: User interest notifier

## Usage

All tools follow the same interface:

def tool_function(params: dict) -> dict:
    """Returns dict with 'status' and optional data"""
    return {"status": "success", "data": ...}

## Adding New Tools

    Create new tool file in appropriate location

    Implement required function

    Add to dispatcher if needed

    Update assistant tool definitions
