from django.urls import path, include
from apps.product import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.all_products, name='empty-paht'),
    path('product/<int:pk>/', views.detail_product, name='product_detail'),
    path('wishlist/', views.view_favorites, name='wishlist'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_favorite/<int:pk>/', views.remove_favorite_list, name='remove_favorite'),
    path('cart/', views.views_cart, name='cart'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('clear_cart/', views.clear_cart, name = 'clear_cart'),
    path('product_search/', views.product_search, name='product_search'),
]