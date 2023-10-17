from django.urls import path
from .views import UserLoginView, UserRegisterView, refresh_token_view

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("refresh/", refresh_token_view, name="refresh"),
]
