# django imports
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.encoding import smart_str, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

# rest_framework imports
from rest_framework import generics, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# 3rd party imports
import jwt

# application imports
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    ResetPasswordEmailRequestSerializer,
    PasswordCheckTokenSerializer,
    SetNewPasswordSerializer,
)
from .token import generate_access_token, generate_refresh_token


# Create your views here.

User = get_user_model()


# register view
class UserRegisterView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# login view
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        email = request.data.get("email", "")
        password = request.data.get("password", "")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(email=email.lower())
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("user with that email does not exist")

        if user.auth_provider != "email":
            raise exceptions.AuthenticationFailed(
                _(f"Please continue your login using {user.auth_provider}")
            )

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response()

        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        serialized_user = UserSerializer(user).data

        response.data = {"access_token": access_token, "user": serialized_user}

        return response


# logout view
def logout_view(request):
    return Response("sucessfully logged out")


# refresh view
@api_view(["POST"])
def refresh_token_view(request):
    refresh_token = request.COOKIES.get("refresh_token")

    if refresh_token is None:
        raise exceptions.AuthenticationFailed(
            "Authentication credentials were not provided"
        )

    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )

    except jwt.DecodeError:
        raise exceptions.AuthenticationFailed("invalid token.")

    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            "refresh token expired login please login again."
        )

    user = User.objects.filter(email=payload["email"]).first()
    access_token = generate_access_token(user)

    return Response({"access_token": access_token})


class ResetPasswordEmailRequestAPIView(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"sucess": "we have sent you a link to reset your password"},
            status=status.HTTP_200_OK,
        )


class PasswordCheckTokenAPIView(generics.GenericAPIView):
    serializer_class = PasswordCheckTokenSerializer

    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response(
                    {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
                )

        except User.DoesNotExist:
            return Response("Invalid link", status=status.HTTP_401_UNAUTHORIZED)
        except DjangoUnicodeDecodeError:
            return Response(
                {"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
            )

        return Response(
            {
                "sucess": True,
                "message": "Valid Credentials",
                "uidb64": uidb64,
                "token": token,
            },
            status=status.HTTP_200_OK,
        )


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(
            {"success": True, "message": "password reset success"},
            status=status.HTTP_200_OK,
        )
