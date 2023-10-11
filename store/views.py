# django imports
from django.utils.decorators import method_decorator

# rest_framework imports
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# 3rd party imports
from drf_yasg.utils import swagger_auto_schema

# applications imports
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from .permissions import IsStaff


# Create your views here.


# for CRUD operations on the product model
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    parser_classes = [MultiPartParser, FormParser]
    queryset = Product.objects.all()
    permission_classes = [IsStaff, IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()

        # increase product populaarity when a customer views the product
        if not (request.user.is_staff) and not (request.user.superuser):
            product.popularity += 1
            product.save()

        serializer = self.serializer_class(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


@method_decorator(
    name="list",
    decorator=swagger_auto_schema(
        operation_description="returns list of all categories.",
        operation_summary="categories list",
    ),
)
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsStaff, IsAuthenticated]
