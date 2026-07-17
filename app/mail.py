import os
import random
import resend
from dotenv import load_dotenv

load_dotenv()

resend.api_key = os.getenv("RESEND_API_KEY")

EMAIL = os.getenv("EMAIL_ADDRESS")


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

    try:

        resend.Emails.send({

            "from": f"Smart Inventory <{EMAIL}>",

            "to": [receiver_email],

            "subject": subject,

            "text": body

        })

        print("OTP Sent Successfully")

        return True

    except Exception as e:

        print("Email Error:", e)

        return False