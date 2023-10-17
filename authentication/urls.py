from django.urls import path
from .views import (
    UserLoginView,
    UserRegisterView,
    refresh_token_view,
    ResetPasswordEmailRequestAPIView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("refresh/", refresh_token_view, name="refresh"),
    path("reset-password/", ResetPasswordEmailRequestAPIView.as_view(), name="reset"),
]
