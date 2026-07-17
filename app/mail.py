import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
SENDER_EMAIL = os.getenv("EMAIL_ADDRESS")


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(receiver_email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json",
    }

    payload = {
        "sender": {
            "name": "Smart Inventory",
            "email": SENDER_EMAIL
        },
        "to": [
            {
                "email": receiver_email
            }
        ],
        "subject": "Smart Inventory - Password Reset OTP",
        "htmlContent": f"""
        <h2>Password Reset OTP</h2>

        <p>Hello,</p>

        <p>Your OTP is:</p>

        <h1>{otp}</h1>

        <p>This OTP is valid for 5 minutes.</p>

        <p>If you didn't request this, ignore this email.</p>

        <br>

        <b>Smart Inventory Team</b>
        """
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        if response.status_code == 201:
            print("OTP Sent Successfully")
            return True

        print(response.text)
        return False

    except Exception as e:
        print(e)
        return False