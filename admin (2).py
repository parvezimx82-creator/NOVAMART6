from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "seller", "category", "price", "stock", "status", "updated_at")
    list_filter = ("status", "category", "created_at")
    search_fields = ("name", "slug", "seller__username")
    list_editable = ("price", "stock", "status")
    prepopulated_fields = {"slug": ("name",)}
