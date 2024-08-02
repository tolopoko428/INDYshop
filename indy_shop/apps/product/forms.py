from django import forms
from .models import Orders, OrderItem, ShippingOption
from django.contrib.auth import get_user_model

class AddToFavoritesForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

class ProductSearchForm(forms.Form):
    name = forms.CharField(label='Поиск по названию', required=False)
    



class OrderForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)
    address = forms.CharField(max_length=100, required=False)
    mobile = forms.CharField(max_length=15, required=False)
    postal_code = forms.CharField(max_length=10, required=False)
    orders_text = forms.CharField(widget=forms.Textarea, required=False)
    shipping_option_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Orders
        fields = [ 'orders_text', 'postal_code']




class ShippingOptionForm(forms.Form):
    shipping_option = forms.ModelChoiceField(
        queryset=ShippingOption.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )

