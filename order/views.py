from django.shortcuts import render
from rest_framework import viewsets,exceptions
from rest_framework.response import Response
from rest_framework import status
from .serializers import OrderSerializer
from .models import Order,OrderItem
from product.models import Product
from django.contrib.auth import get_user_model
# Create your views here.
User = get_user_model()

class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    
    #create Order
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if not data.items:
            return Response({"detail":"No Order Items"},status=status.HTTP_400_BAD_REQUEST)
        
        items = data.pop('items')
        
        try:
            order = Order(**data)
            #testing to set to request.user
            order.owner = User.objects.get(email="kolawolecoke@gmail.com")
            order.save()
            for item in items:
                product = Product.objects.get(id = item.get("product"))
                item = OrderItem.objects.create(product=product,
                                                qty=item['qty'],
                                                order=order)
        except Exception as e:
              return Response(f"validation error {e}",status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order) 
            
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    #Update Orders
    def update(self,request,*args, **kwargs):
        data = request.data
        primary_key = int(kwargs.get("pk"))
        
        if not data.items:
            return Response({"detail":"No Order Items"},status=status.HTTP_400_BAD_REQUEST)
        
        items = data.pop('items')
        
        order = Order.objects.get(id=primary_key)
        order.items.all().delete()
        
        for item in items:
                product = Product.objects.get(id = item.get("product"))
                item = OrderItem.objects.create(product=product,
                                                qty=item['qty'],
                                                order=order)
                
        print(order.items.all())
        order.first_name = data.get("first_name")
        order.last_name = data.get("last_name")
        order.email = data.get("email")
        order.phone = data.get("phone")
        order.postal_code  = data.get("postal_code")
        order.city = data.get("city")
        order.address1 = data.get("address1")
        order.address2 = data.get("address2")
        
        serializer = OrderSerializer(order)
        
        return Response(serializer.data,status=status.HTTP_200_OK)