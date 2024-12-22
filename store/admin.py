from django.contrib import admin

from store.models import City, Store, WareHouse, StoreCity


# Register your models here.
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(StoreCity)
class StoreCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'store', 'city')
    list_filter = ('store', 'city')
    search_fields = ('store__name', 'city__name')


@admin.register(WareHouse)
class WareHouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'store_city', 'address')
    list_filter = ('store_city',)
    search_fields = ('store_city', 'address')
