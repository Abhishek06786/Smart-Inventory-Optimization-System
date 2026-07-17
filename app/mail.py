import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

EMAIL = os.getenv("EMAIL_ADDRESS")
BREVO_API_KEY = os.getenv("BREVO_API_KEY")


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(receiver_email, otp):

    print("EMAIL_ADDRESS:", EMAIL)
    print("BREVO_API_KEY Loaded:", "YES" if BREVO_API_KEY else "NO")

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

    data = {
        "sender": {
            "name": "Smart Inventory",
            # Verified sender
            "email": "abhishekchoubey012@gmail.com"
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "subject": subject,
        "textContent": body
    }

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    try:

        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            json=data,
            headers=headers,
            timeout=30
        )

        print("Status Code:", response.status_code)
        print("Brevo Response:", response.text)

        if response.status_code == 201:
            print("OTP Email Sent Successfully")
            return True

        print("Brevo Error:", response.text)
        return False

    except Exception as e:
        print("Email Error:", str(e))
        return False