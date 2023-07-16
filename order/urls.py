from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    path("user/orders/", views.UserListCreateOrderAPIView.as_view()),
    path("user/orders/<str:id>/", views.UserRetrieveOrderAPIView.as_view()),
    path("orders/paid/", views.update_order_paid),
]
