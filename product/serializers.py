from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
