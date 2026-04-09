from rest_framework import serializers
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    in_stock      = serializers.SerializerMethodField()

    # use_url=True  → returns full URL like http://127.0.0.1:8000/media/products/iphone.jpg
    # allow_null=True → works even when no image uploaded
    image = serializers.ImageField(use_url=True, allow_null=True, required=False)

    class Meta:
        model  = Product
        fields = [
            'id', 'name', 'description',
            'category', 'category_name',
            'price', 'rating', 'stock', 'in_stock',
            'brand', 'image',
            'is_featured', 'created_at',
        ]

    def get_in_stock(self, obj):
        return obj.stock > 0
