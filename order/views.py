from django.http import Http404
from rest_framework import generics,viewsets,mixins
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from .serializers import OrderSerializer,OrderItemSerializer
from .models import Order,OrderItem
from product.models import Product
from django.contrib.auth import get_user_model
from .permissions import IsOrderOwner
from typing import Type

# Create your views here.
User = get_user_model()

class OrderViewset(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [IsAuthenticated,IsOrderOwner]
    
    
    def get_order(self, pk:int) -> Type[Order]:
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
    
    #create Order
    def create(self, request, *args, **kwargs):
        data = request.data
        
        if not data.get("items"):
            return Response({"detail":"No Order Items"},status=status.HTTP_400_BAD_REQUEST)
        
        items = data.pop('items')
        
        try:
            order = Order(**data)
            #testing to change to request.user
            order.owner = request.user
            order.save()
            for item in items:
                product = Product.objects.get(id = item.get("product"))
                item = OrderItem.objects.create(product=product,
                                                qty=item['qty'],
                                                order=order)
                product.count_instock -=item.qty
                product.save()
                    
        except Exception as e:
              return Response(f"validation error {e}",status=status.HTTP_400_BAD_REQUEST)
        
        serializer = OrderSerializer(order) 
            
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    
    #Update Orders
    def update(self,request,*args, **kwargs):
        data = request.data
        pk = int(kwargs.get("pk"))
        
        if not data.get("items"):
            return Response({"detail":"No Order Items"},status=status.HTTP_400_BAD_REQUEST)
        
        items = data.pop('items')
        
        
        order = self.get_order(pk)
        old_items_id = {item.id for item in order.items.all()}
        new_items_id = {item.get("id") for item in items if item.get("id")!=None}
        
        #delete removed order items
        for item in old_items_id:
            if item not in new_items_id:
                item = OrderItem.objects.get(id=item)
                product = item.product
                product.count_instock += item.qty
                product.save()
                item.delete()
            
        for item in items:
                product = Product.objects.get(id = item.get("product"))
                
                if item.get("id"):
                    old_item = OrderItem.objects.get(id=item.get("id"))
                    
                    if item.get("qty")>old_item.qty:
                        qty = item.get("qty")-old_item.qty
                        product.count_instock -=qty 
                        old_item.qty = item.get("qty")
                        
                    elif item.get("qty")<old_item.qty:
                        qty = old_item.qty -item.get("qty")
                        product.count_instock+=qty
                        old_item.qty = item.get("qty")
                        
                    product.save()
                    old_item.save()
                    
                else:
                    new_item = OrderItem.objects.create(product=product,
                                                qty=item['qty'],
                                                order=order)
                    
                    product.count_instock-=new_item.qty
                    product.save()
                
        # order.first_name = data.get("first_name")
        # order.last_name = data.get("last_name")
        # order.email = data.get("email")
        # order.phone = data.get("phone")
        # order.postal_code  = data.get("postal_code")
        # order.city = data.get("city")
        # order.address1 = data.get("address1")
        # order.address2 = data.get("address2")
        
        serializer = OrderSerializer(order,data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, request, *args, **kwargs):
        pk = int(kwargs['pk'])
        #get specific order based of pk
        order = self.get_order(pk)
         
        items = order.items.all()
        
        #loop through all order-items get the product and restore the count in stock if order is not paid
        for item in items:
            product = item.product
            if not order.is_paid:
                product.count_instock += item.qty
                product.save()
                
        #finnally delete order   
        order.delete()
        return Response(pk,status=status.HTTP_204_NO_CONTENT)
    
#updates the order paid field to True
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_order_paid(request,pk):
    try:
        order = Order.objects.get(id=pk)
    except Order.DoesNotExist:
        raise Http404
    
    order.is_paid = True

    return Response("order was paid",status=status.HTTP_200_OK)

        