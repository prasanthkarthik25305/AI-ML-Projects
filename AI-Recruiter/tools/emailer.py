# tools/emailer.py

import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

def send_email(to_email, subject, body, simulate=True):
    if simulate or not EMAIL_ADDRESS or not EMAIL_PASSWORD:
        print(f"\n📤 Simulated Email Sent")
        print(f"To: {to_email}")
        print(f"Subject: {subject}")
        print(f"Body:\n{body}")
        return

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = to_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")

if __name__ == "__main__":
    test_email = "john.doe@example.com"
    subject = "Test Interview Invitation"
    body = """
    Dear John Doe,

    We'd like to invite you for an interview for the role of AI Engineer.

    Please choose a time slot:
    - Monday 10AM
    - Tuesday 10AM

    Thanks,
    AI Recruiter Team
    """
    send_email(test_email, subject, body, simulate=True)
