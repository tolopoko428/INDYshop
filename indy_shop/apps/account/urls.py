from django.urls import path
from apps.account import views


urlpatterns = [
    path('registration/', views.register_user, name = 'register'),
    path('login/', views.LoginView.as_view(), name = 'login'),
    path('index/', views.index, name='index'),
]

