# Purpose: Tool to record user interest/contact info.

from app.tools.dispatcher import send_notification

def record_user_details(email: str, name: str = "Not provided", notes: str = "None") -> dict:
    message = f"[Interest] Email: {email} | Name: {name} | Notes: {notes}"
    send_notification(message)
    return {"status": "recorded"}
