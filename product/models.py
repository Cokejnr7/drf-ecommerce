from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="images/%Y/%m/%d")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField("Category", blank=True, related_name="products")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=False)
    count_instock = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        if self.count_instock == 0:
            self.in_stock = False
        else:
            self.in_stock = True
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ("name",)
