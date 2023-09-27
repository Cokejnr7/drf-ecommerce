from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions
from decouple import config
from authentication.token import generate_access_token, generate_refresh_token

User = get_user_model()


def register_social_user(user_id, email, provider):
    filtered_user_by_email = User.objects.filter(email=email)

    # check if user with that email is already registered
    if filtered_user_by_email.exists():
        # check if the provider the user using to login is the same as the registered provider
        if provider == filtered_user_by_email[0].auth_provider:
            registered_user = authenticate(
                email=email, password=config("SOCIAL_SECRET")
            )

            return {
                "email": registered_user.email,
                "access_token": generate_refresh_token(registered_user),
                "refresh_token": generate_refresh_token(registered_user),
            }

        # if registered user trying to use different providers with the same email address
        else:
            raise exceptions.AuthenticationFailed(
                _(
                    f"Please continue your login using {filtered_user_by_email[0].auth_provider}"
                )
            )

    # This case user does not exist so we create a new user
    else:
        user = User(email=email)
        user.auth_provider = provider
        user.set_password(config("SOCIAL_SECRET"))
        user.save()

        user = User.objects.get(email=email)

        return {
            "email": user.email,
            "access_token": generate_refresh_token(user),
            "refresh_token": generate_refresh_token(user),
        }
