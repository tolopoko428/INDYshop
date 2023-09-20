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

]