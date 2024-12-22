from rest_framework import serializers
from .models import Product, ProductStock, ProductPhoto


class ProductSerializer(serializers.ModelSerializer):
    photo = serializers.SerializerMethodField()
    description = serializers.SerializerMethodField()
    price = serializers.SerializerMethodField()

    def get_photo(self, obj):
        city_id = self.context.get('city_id')
        photo = obj.product_photo.filter(city_id=city_id).first() or obj.product_photo.first()
        return photo.photo.url if photo else None

    def get_description(self, obj):
        description = obj.product_description.first()
        return description.description if description else None

    def get_price(self, obj):
        stock = obj.product_stock.first()
        return stock.price if stock else None

    class Meta:
        model = Product
        fields = ['id',  'photo', 'description', 'price']


class ProductFullSerializer(ProductSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'photo', 'description', 'price', 'views_count']


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductStock
        fields = ['product', 'ware_house', 'quantity', 'price']