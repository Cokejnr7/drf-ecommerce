from django.urls import path
from . import views


urlpatterns = [
    # user urls
    path(
        "user/orders/",
        views.UserListCreateOrderAPIView.as_view(),
        name="user-list-create",
    ),
    path(
        "user/orders/<str:id>/",
        views.RetrieveOrderAPIView.as_view(),
        name="retrieve-order",
    ),
    path("user/orders/<str:id>/paid/", views.update_order_paid, name="update-paid"),
    # admin urls
    path("admin/orders/<str:id>/", views.RetrieveOrderAPIView.as_view()),
    path("orders/<str:id>/status", views.update_order_status, name="update-status"),
]
