from django.urls import path
from .views import (
    UserLoginView,
    UserRegisterView,
    refresh_token_view,
    ResetPasswordEmailRequestAPIView,
    PasswordCheckTokenAPIView,
    SetNewPasswordAPIView,
)

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("refresh/", refresh_token_view, name="refresh"),
    path(
        "request-reset-email/",
        ResetPasswordEmailRequestAPIView.as_view(),
        name="request-reset-email",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        PasswordCheckTokenAPIView.as_view(),
        name="password-reset-confirm",
    ),
    path(
        "password-reset-complete",
        SetNewPasswordAPIView.as_view(),
        name="password-reset-complete",
    ),
]
