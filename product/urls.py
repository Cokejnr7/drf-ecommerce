from .views import ProductViewSet, CategoryViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", ProductViewSet)
router.register("categories", CategoryViewSet)

urlpatterns = router.urls
