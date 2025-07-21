import os
import requests

def send(message: str):
    try:
        token = os.getenv("PUSHOVER_TOKEN")
        user = os.getenv("PUSHOVER_USER")

        if not token or not user:
            print("Pushover not configured — skipping.")
            return

        requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": token,
                "user": user,
                "message": message,
            },
            timeout=5
        )
    except Exception as e:
        print("Pushover failed:", e)
