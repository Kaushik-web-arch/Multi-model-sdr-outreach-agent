from __future__ import annotations
import smtplib
from email.message import EmailMessage
from src.settings import Settings

class SafeEmailSender:
    def __init__(self, settings: Settings):
        self.settings = settings

    def send(self, to_email: str, subject: str, body: str) -> str:
        if not self.settings.allow_email_send:
            return (
                "DRY RUN: email sending is disabled. "
                "Set ALLOW_EMAIL_SEND=true only after we configure SMTP credentials."
            )
        if not to_email:
            return "Not sent: recipient email is empty."
        if not subject or not body:
            return "Not sent: subject/body is empty."
        if not self.settings.smtp_user or not self.settings.smtp_password:
            return "Not sent: SMTP_USER / SMTP_PASSWORD are not configured."

        sender = self.settings.smtp_from or self.settings.smtp_user
        message = EmailMessage()
        message["From"] = sender
        message["To"] = to_email
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP_SSL(self.settings.smtp_host, self.settings.smtp_port, timeout=30) as smtp:
            smtp.login(self.settings.smtp_user, self.settings.smtp_password)
            smtp.send_message(message)
        return f"Sent successfully to {to_email}."
