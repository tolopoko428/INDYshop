from django.urls import path, include
from apps.product import views


urlpatterns = [
    path('index/', views.my_view, name='index-7.html')
]