from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField()
    description = models.TextField(blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=100)
