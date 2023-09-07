from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'created_at', 'stock_count', 'category_id')
    list_filter = ('category_id', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)