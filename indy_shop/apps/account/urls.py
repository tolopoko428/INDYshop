from django.urls import path
from apps.account import views



urlpatterns = [
    path('registration/', views.register_user, name='registration'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('dashboard/logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
]


