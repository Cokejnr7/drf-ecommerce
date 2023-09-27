from rest_framework import serializers, exceptions
from . import google
from django.utils.translation import gettext_lazy as _
from decouple import config


class GoogleAuthSerializer(serializers.Serializer):
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = google.Google.validate(auth_token)
        try:
            user_data["sub"]

        except KeyError:
            raise serializers.ValidationError(
                _("The token is either invalid or expired")
            )

        if user_data.get("aud") != config("GOOGLE_CLIENT_ID"):
            raise exceptions.AuthenticationFailed("oops, unexpected client")

        user_id = user_data.get("sub")
        email = user_data.get("email")
        name = user_data.get("name")
        provider = user_data.get("provider")

        return register_social_user(
            user_id=user_id, email=email, name=name, provider=provider
        )
