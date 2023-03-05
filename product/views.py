from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer
from .models import Product
from .permissions import IsStaff
# Create your views here.

class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsStaff,IsAuthenticated]