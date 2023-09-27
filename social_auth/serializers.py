# django imports
from django.utils.translation import gettext_lazy as _

# rest_framework imports
from rest_framework import serializers, exceptions

# 3rd party libraries
from decouple import config

# application imports
from . import google
from .register import register_social_user


class GoogleLoginSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]

        except:
            raise serializers.ValidationError(
                _("The token is either invalid or expired")
            )

        if user_data.get("aud") != config("GOOGLE_CLIENT_ID"):
            raise exceptions.AuthenticationFailed("oops, unexpected client")

        user_id = user_data.get("sub")
        email = user_data.get("email")
        provider = user_data.get("iss").split(".")[1]

        return register_social_user(user_id, email, provider)
