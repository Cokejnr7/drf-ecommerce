from django.urls import path
from . import views


urlpatterns = [
    # user urls
    path(
        "orders/",
        views.ListCreateOrderAPIView.as_view(),
        name="list-create-order",
    ),
    path(
        "orders/<str:id>/",
        views.RetrieveOrderAPIView.as_view(),
        name="retrieve-order",
    ),
    path("orders/<str:id>/paid/", views.update_order_paid, name="update-paid"),
    path("orders/<str:id>/status/", views.update_order_status, name="update-status"),
]
