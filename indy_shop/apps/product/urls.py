from django.urls import path, include
from apps.product import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.all_products, name='empty-paht'),
    path('product/<int:pk>/', views.detail_product, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_order, name='add_to_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('view_orders/', views.view_orders, name='view_orders'),
    path('wishlist/', views.view_favorites, name='wishlist'),
    path('add_to_favorites/<int:product_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('remove_favorite/<int:pk>/', views.remove_favorite_list, name='remove_favorite'),
]