from django.urls import path
from .views import UserLoginView, UserCreateView, refresh_token_view

urlpatterns = [
    path("register/", UserCreateView.as_view()),
    path("login/", UserLoginView.as_view()),
    path("refresh/", refresh_token_view),
]
