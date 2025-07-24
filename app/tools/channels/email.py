import os
import smtplib
from email.message import EmailMessage
from app.assistant.config.non_ai import config

def send(message: str):
    try:
        sender = os.getenv("SMTP_SENDER")
        password = os.getenv("SMTP_PASSWORD")
        recipient = os.getenv("SMTP_RECIPIENT")
        server = os.getenv("SMTP_SERVER", "smtp.gmail.com")

        if not sender or not password or not recipient:
            print(config.ERRORS["email_not_configured"])
            return

        msg = EmailMessage()
        msg.set_content(message)
        msg["Subject"] = config.NOTIFICATIONS["email_subject"]
        msg["From"] = sender
        msg["To"] = recipient

        with smtplib.SMTP_SSL(server, 465) as smtp:
            smtp.login(sender, password)
            smtp.send_message(msg)
    except Exception as e:
        print(config.ERRORS["email_failed"].format(error=e))
