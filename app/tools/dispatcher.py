# app/tools/dispatcher.py
from tenacity import retry, stop_after_attempt, wait_exponential
from app.tools.channels import pushover, email, slack
from app.assistant.config.non_ai import config
import logging

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def send_with_retry(channel, message):
    return channel.send(message)
    
def send_notification(message: str, notification_type: str = "info"):
    """Send message via all configured notification channels."""
    
    # Add emoji prefix based on type
    if notification_type == "warning":
        message = f"⚠️ {message}"
    elif notification_type == "error":
        message = f"❌ {message}"
    elif notification_type == "success":
        message = f"✅ {message}"
    
    # Try each channel and collect results
    results = {
        "pushover": pushover.send(message),
        "email": email.send(message),
        "slack": slack.send(message)
    }
    
    logger.info(f"Notification dispatched to channels: {results}")
    return results
