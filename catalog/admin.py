from django.contrib import admin
from .models import Product, ProductPhoto, ProductDescription, ProductStock


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'views_count')
    search_fields = ('name', 'views_count')

@admin.register(ProductStock)
class ProductStockAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'ware_house', 'quantity', 'price')
    search_fields = ('product__name', 'ware_house__address')

@admin.register(ProductPhoto)
class ProductPhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'photo', 'city')
    list_filter = ('product',)


@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'description')



