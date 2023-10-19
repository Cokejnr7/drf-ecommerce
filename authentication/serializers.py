from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_bytes,
    smart_str,
    force_str,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework import serializers, exceptions
from .task import send_email

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, write_only=True)

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
            return attrs
        else:
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
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

        finally:
            return super().validate(attrs)


class PasswordCheckTokenSerializer(serializers.Serializer):
    otp = serializers.CharField()
