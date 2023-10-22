# django imports
from django.utils.decorators import method_decorator

# rest_framework imports
from rest_framework import viewsets, status, filters, pagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

# 3rd party imports
from drf_yasg.utils import swagger_auto_schema

# applications imports
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from .permissions import IsStaff


# Create your views here.


class ProductPagination(pagination.PageNumberPagination):
    page_size = 30


# for CRUD operations on the product model
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsStaff, IsAuthenticated]
    pagination_classes = [ProductPagination]
    search_fields = ["^name"]

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()

        # increase product populaarity when a customer views the product
        if not (request.user.is_staff) and not (request.user.superuser):
            product.popularity += 1
            product.save()

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def popular_products(self, request):
        products = self.get_queryset().order_by("-popularity")[:8]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def recent_products(self, request):
        products = self.get_queryset()[:8]
        serializer = self.get_serializer(products, many=True)
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
