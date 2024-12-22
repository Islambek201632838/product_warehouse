from django.db import models
from store.models import WareHouse, City

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название товара")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Количество просмотров")

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=['name'], name='product_name_idx'),
        ]

class ProductPhoto(models.Model):
    product = models.ForeignKey(Product, verbose_name="Товар", on_delete=models.CASCADE, related_name="product_photo")
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.CASCADE, related_name="product_photo", null=True, blank=True, default=None)
    photo = models.ImageField(upload_to='media/product_photos/', verbose_name="Фото товара",
                              default='media/product_photos/Screenshot from 2024-12-22 21-40-31', blank=True)

    def __str__(self):
        return f'photo of {self.product.name}'

    class Meta:
        verbose_name = "Товар и фото"
        verbose_name_plural = "товары и фото"
        indexes = [
            models.Index(fields=['product', 'city'], name='productphoto_product_city_idx'),
        ]

class ProductDescription(models.Model):
    product = models.ForeignKey(Product, verbose_name="товар", on_delete=models.CASCADE, related_name="product_description")
    description = models.TextField(verbose_name="Описание товара")

    def __str__(self):
        return f'description of {self.product.name}'

    class Meta:
        verbose_name = "Товар и описание"
        verbose_name_plural = "товары и их описание"
        indexes = [
            models.Index(fields=['product'], name='productdescription_product_idx'),
        ]

class ProductStock(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Товар", related_name="product_stock")
    ware_house = models.ForeignKey(WareHouse, on_delete=models.CASCADE, verbose_name="Склад", related_name="product_stock")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена (TГ)")

    def __str__(self):
        return f'остатки {self.product.name} ({self.ware_house})'

    class Meta:
        verbose_name = "Остатки Товара"
        verbose_name_plural = "Остатки Товаров"
        unique_together = ('product', 'ware_house')
        indexes = [
            models.Index(fields=['product', 'ware_house'], name='product_stock__idx'),
        ]
