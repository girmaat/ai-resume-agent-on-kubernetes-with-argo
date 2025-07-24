from app.tools.dispatcher import send_notification
from app.assistant.config.non_ai import config
import logging

logger = logging.getLogger(__name__)

def record_user_details(email: str, name: str = "Not provided", notes: str = "None") -> dict:
    try:
        message = (
            f"New Contact Request\n"
            f"Profile: {config.CURRENT_PROFILE}\n"
            f"Name: {name}\n"
            f"Email: {email}\n"
            f"Notes: {notes}"
        )
        send_notification(message)
        logger.info(f"Recorded user interest from {email}")
        return {"status": "success", "message": "Contact details recorded"}
    except Exception as e:
        logger.error(f"Failed to record user details: {str(e)}")
        return {"status": "error", "message": str(e)}
