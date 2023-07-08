from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import OrderViewset,update_order_paid
router = DefaultRouter()

router.register("orders",OrderViewset)

urlpatterns = router.urls

urlpatterns += [path('orders/paid/',update_order_paid)]