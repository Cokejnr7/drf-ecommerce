from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from .permissions import IsStaff
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Product.objects.all()
    permission_classes = [IsStaff, IsAuthenticated]


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="returns list of all categories.",
        operation_summary="list categories",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsStaff, IsAuthenticated]
