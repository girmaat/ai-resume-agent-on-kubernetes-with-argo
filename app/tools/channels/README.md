# Notification Channels

Implements various notification delivery methods.

## Available Channels

### `email.py`
- SMTP email sender
- Requires environment variables:
  - `SMTP_SERVER`
  - `SMTP_SENDER`
  - `SMTP_PASSWORD`
  - `SMTP_RECIPIENT`

### `pushover.py`
- Pushover notification service
- Requires:
  - `PUSHOVER_TOKEN`
  - `PUSHOVER_USER`

### `slack.py`
- Slack webhook integration
- Requires:
  - `SLACK_WEBHOOK_URL`

## Usage
All channels implement:
```python
def send(message: str) -> None:
    """Sends message through channel"""

## Adding New Channels
    Create new channel file
    Implement send() function
    Add error handling
    Update dispatcher
