from django.contrib import admin
from .models import Category, Product, Like, Profile
from .forms import LikeForm
from django.utils.safestring import mark_safe
import sys


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "image_tag",
        "name",
        "price",
        "available",
        "publication_date",
        "updated",
    ]
    list_display_links = [
        "image_tag",
        "name",
    ]
    # list_filter = ['name', 'available', 'publication_date', 'updated']
    list_editable = ["price", "available"]
    prepopulated_fields = {"slug": ("name",)}
    date_hierarchy = "publication_date"
    search_fields = ["name", "slug"]
    ordering = ["-updated"]

    def image_tag(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" style="width: 72px;" />')
        return None


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "fullname", "address", "mobile", "created"]
    list_filter = ["fullname", "mobile"]


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "grade"]
    list_filter = ["user", "product", "grade"]
    form = LikeForm
