from django.urls import path, include
from apps.admin_panel import views
from django.views.generic import TemplateView

urlpatterns = [
    path('error/', views.error, name='error'),
    path('admin_ponel/', views.admin_ponel, name='admin'),
    path('admin_ponel/add_product/', views.add_product, name='add_product'), 
    path('admin_ponel/product/update/<int:product_id>/', views.update_product, name='update_product'),
    path('admin_ponel/product/<int:pk>/', views.admin_detail_post, name='admin_detail_post'),
    path('admin_ponel/product/delete/<int:pk>/', views.delete_product, name='delete_product'),
    path('admin_ponel/personal_registration/', views.staff_registration, name='personal_registration'),
    path('admin_ponel/admin_order_list/', views.admin_order_list, name='admin_order_list'),
    path('admin_ponel/admin_update_order_status/<int:order_id>/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin_ponel/user_profile/<int:user_id>/', views.user_profile, name='user_profile'),
    path('admin_ponel/product/status_update/<int:product_id>/', views.status_update, name='status_update'),
    path('admin_ponel/product/out_of_stock_products/', views.not_active_products, name='not_active_products'),
    path('admin_ponel/product/admin_order_list/order/<int:user_id>/<int:product_id>/', views.detail_order_user, name='detail_order_user'),
]