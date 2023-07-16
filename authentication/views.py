from django.shortcuts import render
from rest_framework import generics, exceptions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, UserLoginSerializer
from django.contrib.auth import get_user_model
from .token import generate_access_token, generate_refresh_token
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.conf import settings
import jwt


# Create your views here.

User = get_user_model()


# register view
class UserCreateView(generics.GenericAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# login view
class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        data = request.data
        email = data.get("email")
        password = data.get("password")

        if email is None and password is None:
            raise exceptions.AuthenticationFailed("email and password required")

        user = User.objects.filter(email=email).first()

        if user is None:
            raise exceptions.AuthenticationFailed("no user with that email")

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed("wrong password")

        access_token = generate_access_token(user)
        refresh_token = generate_refresh_token(user)

        response = Response()

        response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)

        serialized_user = UserSerializer(user).data

        response.data = {"access_token": access_token, "user": serialized_user}

        return response


#logout view
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
