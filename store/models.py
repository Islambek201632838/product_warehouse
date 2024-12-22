from django.db import models

class City(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название города", db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        indexes = [
            models.Index(fields=["name"], name="city_name_idx"),
        ]


class Store(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название Магазина", db_index=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        indexes = [
            models.Index(fields=["name"], name="store_name_idx"),
        ]


class StoreCity(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, verbose_name="Магазин", related_name="store_city")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="Город", related_name="store_city")

    def __str__(self):
        return f'{self.store.name} {self.city.name}'

    class Meta:
        verbose_name = "Магазин Город"
        verbose_name_plural = "Магазины Город"
        indexes = [
            models.Index(fields=["store", "city"], name="store_city_idx"),
        ]


class WareHouse(models.Model):
    store_city = models.ForeignKey(StoreCity, on_delete=models.CASCADE, verbose_name="Магазин", related_name="ware_house", blank=False, null=True, default=None)
    address = models.TextField(verbose_name="Адрес склада")

    def __str__(self):
        return f'{self.store_city} ({self.address})'

    class Meta:
        verbose_name = "Склад"
        verbose_name_plural = "Склады"
        indexes = [
            models.Index(fields=["store_city"], name="warehouse_store_city_idx"),
        ]
