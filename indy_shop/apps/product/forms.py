from django import forms
from .models import Orders, OrderItem, ShippingOption
from django.contrib.auth import get_user_model

class AddToFavoritesForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())

class ProductSearchForm(forms.Form):
    name = forms.CharField(label='Поиск по названию', required=False)
    



class OrderForm(forms.ModelForm):
    user = get_user_model()

    class Meta:
        model = Orders
        fields = ['total_amount', 'status', 'postal_code', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Устанавливаем пользователя по умолчанию в форме
            self.fields['user'].initial = user
        else:
            # Если пользователя нет, поле пользователя становится обязательным
            self.fields['user'].required = True

    total_price = forms.DecimalField(widget=forms.HiddenInput, initial=0)
    total_cost = forms.DecimalField(widget=forms.HiddenInput, initial=0)





class ShippingOptionForm(forms.Form):
    shipping_option = forms.ModelChoiceField(
        queryset=ShippingOption.objects.all(),
        widget=forms.RadioSelect,
        empty_label=None,
    )

