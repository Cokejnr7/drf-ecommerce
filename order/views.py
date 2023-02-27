from django.shortcuts import render
from rest_framework import viewsets,exceptions
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order,OrderItem
from product.models import Product
# Create your views here.

class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if not data.items:
            return Response({"detail":"No Order Items"},status=status.HTTP_400_BAD_REQUEST)
        
        items = data.pop('items')
        
        try:
            order = Order.objects.create(**data)

            for item in items:
                product = Product.objects.get(id = item.get("product"))
                item = OrderItem.objects.create(product=product,
                                                qty=item['qty'],
                                                order=order)
        except:
              return Response("validation error",status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order) 
            
        return Response(serializer.data,status=status.HTTP_201_CREATED)