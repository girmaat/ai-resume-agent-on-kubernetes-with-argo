# Purpose: Tool to record unknown user questions.

from app.tools.dispatcher import send_notification

def record_unknown_query(question: str) -> dict:
    message = f"[Unknown Question] {question}"
    send_notification(message)
    return {"status": "logged"}
