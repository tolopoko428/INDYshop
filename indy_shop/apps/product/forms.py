from django import forms
from .models import Orders, OrderItem
from django.contrib.auth import get_user_model

class AddToFavoritesForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

class ProductSearchForm(forms.Form):
    name = forms.CharField(label='Поиск по названию', required=False)
    

# class OrderForm(forms.ModelForm):
#     # Получите модель пользователя
#     User = get_user_model()

#     # Установите значения по умолчанию на основе профиля пользователя
#     initial = {
#         'first_name': User.first_name,
#         'last_name': User.last_name,
#         'address': User.address,
#         'email': User.email,
#         'mobile': User.mobile,
#     }

#     class Meta:
#         model = Orders
#         fields = ['total_amount', 'status', 'postal_code', 'first_name', 'last_name', 'address', 'email', 'mobile']