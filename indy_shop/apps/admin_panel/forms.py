from django import forms
from apps.product.models import Product, Category, ProductImage
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from django.contrib.auth.forms import UserCreationForm
from apps.product.models import *
class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True



class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput)
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class CreateProductForm(forms.ModelForm):
    price = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={"type": "number"}))
    category_id = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label=None, label="Категория")
    images = forms.FileField(widget=MultipleFileInput(attrs={'multiple': True}))
    quantity = forms.IntegerField(initial=1)
    color = forms.ChoiceField(choices=COLOR_CHOICES, required=False, label="Цвет")  
    size = forms.ChoiceField(choices=SIZE_CHOICES, required=False, label="Размер") 

    sizes = forms.ModelMultipleChoiceField(
    queryset=Size.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False
    )

    colors = forms.ModelMultipleChoiceField(
    queryset=Color.objects.all(),
    widget=forms.CheckboxSelectMultiple,
    required=False
    ) 

    class Meta:
        model = Product
        exclude = []
        fields = ['title', 'description', 'price', 'category', 'quantity', 'color', 'size', 'images']

    def save(self, commit=True):
        product = super(CreateProductForm, self).save(commit=False)
        product.quantity = self.cleaned_data['quantity']
        product.save()
        images = self.files.getlist('images')
        product.sizes.set(self.cleaned_data['sizes'])
        product.colors.set(self.cleaned_data['colors'])  # Обратите внимание на имя поля 'images'
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product



class ProductImagesForm(forms.ModelForm):
    is_main = forms.BooleanField(required=False, initial=False)  # Добавляем поле для is_main

    class Meta:
        model = ProductImage
        fields = ('image', 'is_main')




class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        image = MultipleFileField(required=False)
        fields = ['title', 'description', 'price', 'stock_count', 'category', 'discount', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'] = MultipleFileField(required=False)




class StaffRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            "email", 
            "first_name", 
            "last_name",
        ]