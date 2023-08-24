from django.urls import path
from apps.account import views


urlpatterns = [
    path('registration/', views.register, name = 'register'),
    path('index/', views.index, name='index')
]

