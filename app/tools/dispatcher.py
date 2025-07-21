# ------------------------------------------------------------------------
# Purpose: Central dispatcher to send a message to all available channels.
# ------------------------------------------------------------------------

from app.tools.channels import pushover, email, slack

def send_notification(message: str):
    """Send message via all configured notification channels."""
    pushover.send(message)
    email.send(message)
    slack.send(message)
