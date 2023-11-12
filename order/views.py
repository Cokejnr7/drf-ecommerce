# django imports
from django.http import Http404
from django.contrib.auth import get_user_model

# rest_framework imports
from rest_framework import generics, viewsets, mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from .serializers import OrderSerializer, OrderItemSerializer

# application imports
from .models import Order, OrderItem
from store.models import ProductVariant
from .permissions import IsStaffOrOrderOwner, IsStaff

# ------ ----- ---- python ---- ----- ------
from typing import Type

# Create your views here.
User = get_user_model()


# get list of user orders or create new order
class UserListCreateOrderAPIView(generics.GenericAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated]
    http_method_names = ["get", "post"]

    def get_queryset(self, request):
        queryset = super().get_queryset()
        if request.user.is_authenticated and not (request.user.is_staff):
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
            # creating new order
            order = Order(**data)
            # testing to change to request.user
            order.owner = request.user
            order.save()

            # looping through the list of item dictionary to create OrderItems
            for item in items:
                product_variant = ProductVariant.objects.get(
                    id=item.get("product_variant")
                )
                item = OrderItem.objects.create(
                    product_variant=product_variant, qty=item["qty"], order=order
                )

                # updating count in stock of the product
                product.count_instock -= item.qty
                product.save()

        except Exception as e:
            return Response(f"validation error {e}", status=status.HTTP_400_BAD_REQUEST)

        serializer = OrderSerializer(order)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# get order by ID
class RetrieveOrderAPIView(generics.GenericAPIView):
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

        self.check_object_permissions(request, order)

        serializer = self.serializer_class(order, many=False)

        return Response(serializer.data, status=status.HTTP_200_OK)


# updates the order paid field to True
@permission_classes([IsAuthenticated, IsStaffOrOrderOwner])
@api_view(["PUT"])
def update_order_paid(request, pk):
    try:
        order = Order.objects.get(pk=id)
    except Order.DoesNotExist:
        raise Http404

    order.is_paid = True
    order.save()
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
