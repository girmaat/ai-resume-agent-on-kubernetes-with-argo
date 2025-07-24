import os
import requests
from app.assistant.config.non_ai import config

def send(message: str):
    try:
        webhook = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook:
            print(config.ERRORS["slack_not_configured"])
            return

        payload = {"text": message}
        requests.post(webhook, json=payload, timeout=5)
    except Exception as e:
        print(config.ERRORS["slack_failed"].format(error=e))
