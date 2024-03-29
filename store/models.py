from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify

# Create your models here.

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(
        upload_to="images/categories/%Y/%m/%d", blank=True, null=True
    )
    slug = models.SlugField(unique=True, blank=True)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="children",
    )
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Size(models.Model):
    name = models.CharField(max_length=100)


class Color(models.Model):
    name = models.CharField(max_length=100)


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to="images/product/%Y/%m/%d", blank=True, null=True
    )
    price = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    categories = models.ForeignKey(
        "Category", on_delete=models.SET_NULL, related_name="products", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    popularity = models.PositiveIntegerField(default=0)
    stock_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    image = models.ImageField(upload_to="images/products/%Y/%m/%d")
    stock_count = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ["product", "size", "color"]

    def __str__(self) -> str:
        return f"{self.product.name}-{self.color}-{self.size}"

    def save(self, *args, **kwargs):
        stock_change = (
            self.stock_count - self.__class__.objects.get(id=self.id)
            if self.id
            else self.stock_count
        )

        self.product.stock_count += stock_change
        self.product.save()
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(
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
