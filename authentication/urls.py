from django.urls import path
from .views import UserLoginView,UserCreateView,refresh_token_view

urlpatterns = [
    path('auth/register',UserCreateView.as_view()),
    path('auth/login',UserLoginView.as_view()),
    path('auth/refresh',refresh_token_view)
]
