import os
import random
import smtplib

from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
PASSWORD = os.getenv("EMAIL_PASSWORD")


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(receiver_email, otp):

    subject = "Smart Inventory - Password Reset OTP"

    body = f"""
Hello,

You requested to reset your Smart Inventory account password.

------------------------------------

Your OTP is:

{otp}

------------------------------------

This OTP is valid for only 5 minutes.

If you did not request this password reset, simply ignore this email.

Regards,

Smart Inventory Team
"""

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = EMAIL
    msg["To"] = receiver_email

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)

        print("OTP Sent Successfully")
        return True

    except Exception as e:
        print("Email Error:", e)
        return False