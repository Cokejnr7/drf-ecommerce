from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_bytes,
    force_str,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import serializers, exceptions
from .task import send_email
from .utils import make_otp

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "id"]

    def validate(self, attrs):
        email = attrs.get("email")
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(_("user with that email already exist"))

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)
    password = serializers.CharField(min_length=8, write_only=True)


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    def validate(self, attrs):
        request = self.context["request"]
        email = attrs.get("email", "")

        try:
            user = User.objects.get(email=email.lower(), auth_provider="email")
        except User.DoesNotExist:
            return super().validate(attrs)
        else:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = make_otp(email)
            current_site = get_current_site(request=request).domain
            relative_link = reverse(
                "password-reset-confirm", kwargs={"uidb64": uidb64, "token": token}
            )
            absurl = "http://" + current_site + relative_link
            email_body = (
                f"Hi {user.email} use the link below to reset your password \n" + absurl
            )
            data = {
                "message": email_body,
                "email": user.email,
                "subject": "Reset your password",
            }
            send_email(**data)

        return super().validate(attrs)


class PasswordCheckTokenSerializer(serializers.Serializer):
    otp = serializers.IntegerField()


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidbase64 = serializers.CharField(min_length=1, write_only=True)

    def validate(self, attrs):
        password = attrs.get("password", "")
        token = attrs.get("token", "")
        uidb64 = attrs.get("uidbase64", "")

        print(password, token, uidb64)

        try:
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise exceptions.AuthenticationFailed("the reset link is invalid", 401)

        except (User.DoesNotExist, DjangoUnicodeDecodeError):
            raise exceptions.AuthenticationFailed("the reset link is invalid", 401)

        else:
            user.set_password(password)
            user.save()

        return super().validate(attrs)
