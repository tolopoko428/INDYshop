from django.urls import path, include
from apps.product import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static
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
    path('product/checkout/', views.checkout, name='checkout'),
    path('order_list/<int:user_id>/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('cancel_order/<int:order_id>/', views.cancel_order, name='cancel_order'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)