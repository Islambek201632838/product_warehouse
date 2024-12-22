from django.contrib import admin
from users.models import CustomUser, CustomerDeliverWareHouse


# Register CustomUser in admin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'city')
    list_filter = ('role',)
    search_fields = ('first_name', 'last_name', 'email')

@admin.register(CustomerDeliverWareHouse)
class CustomerDeliverWareHouseAdmin(admin.ModelAdmin):
    list_display = ('user', 'warehouse')
    list_filter = ('user', 'warehouse')
    search_fields = ('user', 'warehouse')