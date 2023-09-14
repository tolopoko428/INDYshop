from django import forms

class AddToFavoritesForm(forms.Form):
    product_id = forms.IntegerField(widget=forms.HiddenInput())



