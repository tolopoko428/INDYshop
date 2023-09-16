from django.urls import path
from apps.account import views


urlpatterns = [
    #profile ponel
    path('registration/', views.register_user, name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('profile/logout/', views.user_logout, name='logout'),
    path('profile/', views.update_profile, name='profile'),
    path('profile/dashboard/', views.dashboard, name='dashboard'),
    path('profile/dashboard/edit_address/', views.edit_address, name='edit_address'),
    path('contact/', views.views_contact, name='contact'),
]


