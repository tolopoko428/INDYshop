from django import forms
from django.contrib.auth.forms import UserCreationForm
from apps.account.models import User



class UserRegisterForm(forms.Form):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)



