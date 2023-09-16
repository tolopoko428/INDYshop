from django.urls import path, include
from apps.product import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.all_products, name='empty-paht'),
    path('product/<int:pk>/', views.detail_product, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_order, name='add_to_cart'),
    path('checkout/', views.cart_items, name='checkout'),
    path('cart/', views.view_orders, name='cart'),
    path('wishlist/', views.view_favorites, name='wishlist'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_favorite/<int:pk>/', views.remove_favorite_list, name='remove_favorite'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_order, name='remove_from_cart'),
]