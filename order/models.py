from django.db import models
from product.models import Product
# Create your models here.


class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        
        
    def __str__(self) -> str:
        return f"{self.first_name}  {self.last_name}"
    
        
class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,related_name="items", null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.ImageField()
    id = models.AutoField(primary_key=True, unique=True, editable=False)
    
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.image = self.product.image
        return super.save( *args, **kwargs)
    
    @property
    def get_cost(self):
        return self.qty*self.price
