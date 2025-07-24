import os
import requests
from app.assistant.config.non_ai import config

def send(message: str):
    try:
        token = os.getenv("PUSHOVER_TOKEN")
        user = os.getenv("PUSHOVER_USER")

        if not token or not user:
            print(config.ERRORS["pushover_not_configured"])
            return
        title = config.NOTIFICATIONS.get("email_subject", "AI Assistant Notification")
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": token,
                "user": user,
                "message": message,
                "title": title,
                "priority": 1,  # High priority (-2 to 2)
                "sound": "intermission"  # Custom sound
            },
            timeout=10
        )
    except Exception as e:
        print(config.ERRORS["pushover_failed"].format(error=e))
