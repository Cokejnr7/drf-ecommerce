from django.db import models
from product.models import Product
from django.contrib.auth import get_user_model
from .validators import validate_item_price

# Create your models here.

User = get_user_model()


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "PNDG", "pending"
        DELIVERED = "DELV", "delivered"
        IN_TRANSIT = "INTNS", "inTransit"
        CANCELLED = "CNXLD", "cancelled"

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address1 = models.CharField(max_length=250)
    address2 = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_paid = models.BooleanField(default=False)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    # payment_method  =

    class Meta:
        ordering = ("-created",)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items)


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
        null=True,
        blank=True,
    )
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="items", null=True, blank=True
    )
    name = models.CharField(max_length=200, blank=True)
    qty = models.IntegerField(null=False, blank=False)
    price = models.DecimalField(
        default=0.00,
        max_digits=7,
        decimal_places=2,
        blank=True,
        validators=[validate_item_price],
    )
    id = models.AutoField(primary_key=True, unique=True, editable=False)

    def get_cost(self):
        return self.qty * self.price

    def save(self, *args, **kwargs):
        self.price = self.product.price
        self.name = self.product.name
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name
