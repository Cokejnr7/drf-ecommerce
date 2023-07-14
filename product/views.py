from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from .permissions import IsStaff

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Product.objects.all()
    permission_classes = [IsStaff, IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsStaff, IsAuthenticated]
