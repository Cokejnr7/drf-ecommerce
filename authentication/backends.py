from rest_framework import authentication, exceptions
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class JWTAuthentication(authentication.BasicAuthentication):
    def authenticate(self, request):
        authorization_header = authentication.get_authorization_header(request)

        if not authorization_header:
            return

        auth = authorization_header.decode("utf-8").split(" ")

        if len(auth) < 2:
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided or are invalid."
            )

        prefix, token = auth

        if prefix != "Bearer":
            raise exceptions.AuthenticationFailed(
                "Authentication credentials were not provided or are invalid (Expected Bearer token type)"
            )

        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[
                    settings.ALGORITHM,
                ],
            )
            user = User.objects.get(email=payload["email"])

            return (user, token)

        except jwt.DecodeError:
            raise exceptions.AuthenticationFailed("invalid token")

        except jwt.ExpiredSignatureError:
            raise exceptions.AuthenticationFailed("token expired")
