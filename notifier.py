from typing import Optional
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class Notifier:
    def __init__(self, smtp_server: str, smtp_port: int, email: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.email = email
        self.password = password

    def send_email(self, subject: str, message: str, recipient: str) -> bool:
        """Send an email notification."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = recipient
            msg['Subject'] = subject

            msg.attach(MIMEText(message, 'plain'))

            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            print(f"Failed to send email notification: {e}")
            return False

    def notify_queue_position(self, position: int, threshold: int, recipient: str) -> None:
        """Send a notification about queue position."""
        subject = f"Queue Position Update: {position}"
        message = f"Current queue position: {position}\nThreshold: {threshold}"
        self.send_email(subject, message, recipient) 