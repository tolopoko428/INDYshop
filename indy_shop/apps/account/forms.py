from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm

from apps.account.models import User


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Электронная почта",
        widget=forms.EmailInput(attrs={"class":"main-input-box", "placeholder":"example@example.com"})
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class":"main-input-box"})
    )



class UserRegisterForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput())

    class Meta: 
        model = User
        fields = [
            "email", 
            "first_name", 
            "last_name",
            ]
        


class UpdateProfileForm(forms.ModelForm):
    current_password = forms.CharField(
        label='Текущий пароль',
        widget=forms.PasswordInput,
        required=True
    )
    new_password = forms.CharField(
        label='Новый пароль',
        widget=forms.PasswordInput,
        required=False
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'address', 'mobile']

    def clean_current_password(self):
        current_password = self.cleaned_data.get('current_password')
        if not self.instance.check_password(current_password):
            raise forms.ValidationError('Неправильный текущий пароль')
        return current_password

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


class AddressForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['address']  # Укажите все поля, которые вы хотите редактировать

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['address'].widget.attrs.update({'class': 'form-control'})
