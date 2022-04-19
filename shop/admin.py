from django.contrib import admin
from .models import Category, Product, Gallery, Comment, Brand


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'updated', 'brand']
    list_filter = ['available', 'created', 'updated', 'brand']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['image', 'product']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'product', 'created', 'active', 'rating']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']