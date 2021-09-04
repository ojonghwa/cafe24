from django.contrib import admin
from .models import Category, Product, Like, Profile
from .forms import LikeForm


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'publication_date', 'updated']
    list_filter = ['name', 'available', 'publication_date', 'updated']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    date_hierarchy = 'publication_date'
    search_fields = ['name']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'fullname', 'address', 'mobile', 'created']
    list_filter = ['fullname', 'mobile']


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'grade']
    list_filter = ['user', 'product', 'grade']
    form = LikeForm

