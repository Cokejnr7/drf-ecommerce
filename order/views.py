from django.http import Http404
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import OrderSerializer, OrderItemSerializer
from .models import Order, OrderItem
from product.models import Product
from django.contrib.auth import get_user_model
from .permissions import IsStaffOrOrderOwner
from typing import Type

# Create your views here.
User = get_user_model()


# get user orders or create new order
class UserListCreateOrderAPIView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self, request):
        queryset = super().get_queryset()
        queryset = queryset.filter(owner=request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        user_orders = self.get_queryset(request)
        serializer = self.serializer_class(user_orders, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    # create Order
    def post(self, request, *args, **kwargs):
        data = request.data

        if not data.get("items"):
            return Response(
                {"detail": "No Order Items"}, status=status.HTTP_400_BAD_REQUEST
            )

        items = data.pop("items")

        try:
            order = Order(**data)
            # testing to change to request.user
            order.owner = request.user
            order.save()
            for item in items:
                product = Product.objects.get(id=item.get("product"))
                item = OrderItem.objects.create(
                    product=product, qty=item["qty"], order=order
                )
                product.count_instock -= item.qty
                product.save()

        except Exception as e:
            return Response(f"validation error {e}", status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# get order by ID
class UserRetrieveOrderAPIView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated, IsStaffOrOrderOwner]
    http_method_names = ["get"]

    def get_order(self, pk: int) -> Type[Order]:
        """
        tries to get order by pk
        returns order if order exist with that primary key
        else raises Http404 (not found)
        """
        try:
            order = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise Http404
        return order

    def get(self, request, *args, **kwargs):
        id = int(kwargs["id"])

        order = self.get_order(id)

        serializer = self.serializer_class(order, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


# updates the order paid field to True
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order_paid(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        raise Http404

    order.is_paid = True

    return Response("order was paid", status=status.HTTP_200_OK)


# update order status
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_order_status(request, pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        raise Http404

    # order.status = True

    return Response(
        f"order status updated to {order.status}", status=status.HTTP_200_OK
    )
