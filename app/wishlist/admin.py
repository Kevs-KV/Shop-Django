from django.contrib import admin

# Register your models here.
from wishlist.models import Wishlist


@admin.register(Wishlist)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['user', 'product']