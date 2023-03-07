from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer,CategorySerializer
from .models import Product,Category
from .permissions import IsStaff
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsStaff,IsAuthenticated]
    

class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category
    permission_classes = [IsStaff,IsAuthenticated]