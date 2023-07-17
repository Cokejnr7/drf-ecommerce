from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()


urlpatterns = [
    # user urls
    path("user/orders/", views.UserListCreateOrderAPIView.as_view()),
    path("user/orders/<str:id>/", views.RetrieveOrderAPIView.as_view()),
    path("user/orders/<str:id>/paid/", views.update_order_paid),
    # admin urls
    path("admin/orders/<str:id>/", views.RetrieveOrderAPIView.as_view()),
]
