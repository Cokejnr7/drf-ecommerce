import jwt
from datetime import datetime as dt, timedelta
from django.conf import settings


def generate_access_token(user):
    access_token_payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": dt.utcnow() + timedelta(days=0, minutes=5),
        "iat": dt.utcnow(),
    }

    access_token = jwt.encode(
        access_token_payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        "user_id": user.id,
        "email": user.email,
        "exp": dt.utcnow() + timedelta(days=0, minutes=60),
        "iat": dt.utcnow(),
    }

    refresh_token = jwt.encode(
        refresh_token_payload, settings.JWT_SECRET_KEY, algorithm=settings.ALGORITHM
    )

    return refresh_token
