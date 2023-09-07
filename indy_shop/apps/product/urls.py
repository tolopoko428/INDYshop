from django.urls import path, include
from apps.product import views
from django.views.generic import TemplateView

urlpatterns = [
    path('base', TemplateView.as_view(template_name='base.html'), name='base'),
    path('error/', views.error, name='error'),
    path('add_product/', views.add_product, name='add_product'), 
    path('', views.all_products, name= 'empty-paht'), 

]