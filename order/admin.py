from django.contrib import admin

# Register your models here.
from order.models import Order, Item


class OrderItemInline(admin.TabularInline):
    model = Item
    raw_id_fields = ['product']




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ['first_name', 'last_name', 'email', 'address', 'city', 'country', 'telephone', 'creation_date', 'checked_out']
    list_filter = ['creation_date', 'checked_out']
    inlines = [OrderItemInline]