import pyotp
import base64
from django.conf import settings


def make_otp(email: str):
    email_bytes = email.encode("ascii")
    email_base32 = base64.b32encode(email_bytes).decode("ascii")
    totp = pyotp.TOTP(
        settings.OTP_SECRET_KEY + email_base32, interval=settings.OTP_INTERVAL
    )
    generated_token = totp.now()
    print(totp, generated_token)
    return generated_token


def verify_otp(email, otp):
    email_bytes = email.encode("ascii")
    email_base32 = base64.b32encode(email_bytes).decode("ascii")
    totp = pyotp.TOTP(
        settings.OTP_SECRET_KEY + email_base32, interval=settings.OTP_INTERVAL
    )
    return totp.verify(otp)
