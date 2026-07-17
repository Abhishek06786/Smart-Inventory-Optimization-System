import os
import random
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")

SENDER_EMAIL = "abhishekchoubey012@gmail.com"


def generate_otp():
    return str(random.randint(100000, 999999))


def send_otp(receiver_email, otp):

    url = "https://api.brevo.com/v3/smtp/email"

    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }

    payload = {
        "sender": {
            "name": "Smart Inventory Project",
            "email": SENDER_EMAIL
        },

        "replyTo": {
            "email": SENDER_EMAIL,
            "name": "Smart Inventory Project"
        },

        "to": [
            {
                "email": receiver_email
            }
        ],

        "subject": "Smart Inventory - Password Reset OTP",

        "htmlContent": f"""
        <html>
        <body style="font-family:Arial,sans-serif">

        <h2>Smart Inventory</h2>

        <p>Hello,</p>

        <p>You requested to reset your password.</p>

        <p>Your OTP is:</p>

        <h1 style="color:#2563eb;">{otp}</h1>

        <p>This OTP is valid for <b>5 minutes</b>.</p>

        <p>If you didn't request this password reset, please ignore this email.</p>

        <br>

        <p>Regards,</p>

        <b>Smart Inventory Team</b>

        </body>
        </html>
        """
    }

    try:

        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=20
        )

        print(response.status_code)
        print(response.text)

        if response.status_code == 201:
            print("OTP Sent Successfully")
            return True

        return False

    except Exception as e:
        print("Email Error:", e)
        return False