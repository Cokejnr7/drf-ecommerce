import pyotp
from datetime import datetime as dt
from django.conf import settings


def send_otp(
    email,
):
    totp = pyotp.TOTP(settings.OTP_SECRET + email, interval=settings.OTP_INTERVAL)

    pass


def send_email(data):
    pass
