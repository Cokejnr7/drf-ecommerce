from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.

User = get_user_model()


class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Color"
        verbose_name_plural = "Colors"

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10, unique=True)

    class Meta:
        verbose_name = "Size"
        verbose_name_plural = "Sizes"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to="images/products/%Y/%m/%d")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    colors = models.ManyToManyField(Color, blank=True)
    sizes = models.ManyToManyField(Size, blank=True)
    description = models.TextField(blank=True, null=True)
    categories = models.ManyToManyField("Category", blank=True, related_name="products")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    in_stock = models.BooleanField(default=False)
    count_instock = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)

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
    image = models.ImageField(
        upload_to="images/products/%Y/%m/%d", blank=True, null=True
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)


class Review(models.Model):
    Product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        choices=[(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")]
    )

    class Meta:
        verbose_name = "Review"
        verbose_name_plural = "Reviews"
        unique_together = ["product", "reviewer"]

    def __str__(self) -> str:
        return f"Review by {self.reviewer.email} for {self.product.name}"
