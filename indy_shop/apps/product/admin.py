from django.contrib import admin
from .models import *
from .forms import *
from apps.admin_panel.forms import *
# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):  # You can also use 'StackedInline' for a different display style
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'price', 'created_at', 'stock_count', 'category', 'is_top', 'rating', 'quantity', 'status')
    list_filter = ('category', 'is_top', 'created_at', 'quantity', 'status')
    search_fields = ('title', 'category__name')
    form = ProductEditForm
    inlines = [ProductImageInline]  
    def save_model(self, request, obj, form, change):
        # Ваша логика обновления is_top здесь Incorrect
        if obj.discount > obj.price:
            obj.is_top = True
        else:
            obj.is_top = False
        obj.save()

    def delete_model(self, request, obj):
        # Ваша логика удаления продукта здесь
        obj.delete()



@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'total_amount', 'status', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user_id__username', 'status')

    def user_id(self, obj):
        return obj.user_id.username

    user_id.short_description = 'User'

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()



@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'order_item_id', 'quantity', 'update_at')
    list_filter = ('update_at',)
    search_fields = ('order_id__user_id__username', 'order_item_id__title')

    def order_id(self, obj):
        return obj.order_id.id

    def order_item_id(self, obj):
        return obj.order_item_id.title

    order_id.short_description = 'Order ID'
    order_item_id.short_description = 'Order Item Title'

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()



@admin.register(FavoriteProduct)
class FavoriteProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'user_id')
    search_fields = ('product_id', 'user_id')

    actions = ['delete_selected']

    def delete_selected(self, request, queryset):
        for obj in queryset:
            obj.delete()


@admin.register(ProductImage)
class AdminProductImage(admin.ModelAdmin):
    list_display = ('product', 'image', 'is_main')




@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = ('user',)



@admin.register(CartItem)
class AdminCartItem(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity',)


@admin.register(ShippingOption)
class AdminShippingOption(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')

