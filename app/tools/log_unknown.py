# app/tools/log_unknown.py
from app.tools.dispatcher import send_notification
from app.assistant.config.non_ai import config
import logging

logger = logging.getLogger(__name__)

def record_unknown_query(question: str) -> dict:
    try:
        message = f"Unknown Question\nProfile: {config.CURRENT_PROFILE}\nQuestion: {question}"
        send_notification(message)
        logger.info(f"Logged unknown question: {question}")
        return {"status": "success", "message": "Question logged"}
    except Exception as e:
        logger.error(f"Failed to log unknown question: {str(e)}")
        return {"status": "error", "message": str(e)}
