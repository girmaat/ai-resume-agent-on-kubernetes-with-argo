import os
import requests

def send(message: str):
    try:
        webhook = os.getenv("SLACK_WEBHOOK_URL")
        if not webhook:
            print("Slack not configured — skipping.")
            return

        payload = {"text": message}
        requests.post(webhook, json=payload, timeout=5)
    except Exception as e:
        print("Slack failed:", e)
