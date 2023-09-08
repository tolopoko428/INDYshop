from django import forms
from apps.product.models import Product, Category




class CreateProductForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"type": "number"}))
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, label="Категория")
    
    class Meta:
        model = Product
        exclude = []
        fields = ['title', 'description', 'price', "category_id", "image"]
