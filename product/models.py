from django.db import models

# Create your models here.


class Product(models.Model):
    name = models.CharField(max_length=100,unique=True)
    image = models.ImageField()
    price = models.DecimalField(max_digits=7,decimal_places=2)
    description = models.TextField(blank=True, null=True)
    category = models.ManyToManyField("Category")

class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    
    def __str__(self):
        return self.name
