from django import forms
from apps.product.models import Product, Category, ProductImage
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied


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
    image = MultipleFileField()

    

    class Meta:
        model = Product
        exclude = []
        fields = ['title', 'description', 'price', 'category_id']

    def save(self, commit=True):
        product = super(CreateProductForm, self).save(commit=False)
        product.save()
        images = self.files.getlist('image')  # Получите список выбранных файлов
        for image in images:
            ProductImage.objects.create(product=product, image=image)
        return product


class ProductImagesForm(forms.ModelForm):
    class Meta:
        model = ProductImage
        fields = ('image',)



class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        image = MultipleFileField(required=False)
        fields = ['title', 'description', 'price', 'stock_count', 'category', 'discount']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'] = MultipleFileField(required=False)
