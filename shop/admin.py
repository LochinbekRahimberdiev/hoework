from django.contrib import admin
from .models import Category, Product, Order, Comment

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ['name']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'price', 'discount', 'updated')
    search_fields = ['name', 'slug']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone_number', 'product')
    search_fields = ['name', 'phone_number']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'product', 'message')
    search_fields = ['full_name', 'id']



