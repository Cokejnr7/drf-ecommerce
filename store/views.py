# django imports
from django.utils.decorators import method_decorator

# rest_framework imports
from rest_framework import viewsets, status, filters, pagination
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser

# 3rd party imports
from drf_yasg.utils import swagger_auto_schema

# applications imports
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category
from .permissions import IsStaff
from .filters import PriceRangeFilter


# Create your views here.


class ProductPagination(pagination.PageNumberPagination):
    page_size = 30


# for CRUD operations on the product model
class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsStaff]
    pagination_classes = [ProductPagination]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, PriceRangeFilter]
    search_fields = ["^name"]
    ordering_fields = ["price", "name"]

    def retrieve(self, request, *args, **kwargs):
        product = self.get_object()

        # increase product populaarity when a customer views the product
        if not (request.user.is_staff) and not (request.user.is_superuser):
            product.popularity += 1
            product.save()

        serializer = self.get_serializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # returns the first 8 most popular products
    @action(detail=False, methods=["get"])
    def popular_products(self, request):
        products = self.get_queryset().order_by("-popularity")[:8]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # returns eight of the latest products
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
    permission_classes = [IsStaff]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["^slug"]
    ordering_fields = [
        "slug",
        "created_at",
    ]

    def get_queryset(self):
        queryset = super().get_queryset().filter(parent=None)
        return queryset
