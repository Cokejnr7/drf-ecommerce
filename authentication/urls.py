from django.urls import path
from .views import UserLoginView, UserCreateView, refresh_token_view

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("refresh/", refresh_token_view, name="refresh"),
]
