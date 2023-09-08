from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.

from apps.account.forms import *
from apps.account.models import User


class LoginView(FormView):
    form_class = LoginForm
    template_name ="login.html"

    def form_valid(self, form):
        data = form.cleaned_data #{"password":"admin", "email":"admin@gmail.com"}
        # cleaned_data хранилище данных из формы в виде dict
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email,password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("empty-paht")
            return HttpResponse("Ваш аккаунт не активен!")
        return HttpResponse("Введенные вами данные некорректные!")



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("empty-paht")


def register_user(request):
    template_name='registration.html'
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = User.objects.create(
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
            )
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("empty-paht")
    
    context = {'form':form}
    return render(request, template_name, context)



def index(request):
    template_name = 'base.html'
    return render(request, template_name)



@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)
  


@login_required
def update_profile(request):
    template_name = 'dashboard.html'
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.instance  # Получаем обновленный объект пользователя
            email_changed = form.cleaned_data['email'] != user.email
            password_changed = form.cleaned_data['new_password'] != ''
            
            if email_changed or password_changed:
                # Если email или пароль изменены, обновляем пароль и автоматически залогиниваем пользователя
                form.save()
                login(request, user)
                messages.success(request, 'Ваш профиль был успешно обновлен и вы автоматически вошли в систему.')
                return redirect('dashboard')
            else:
                # В противном случае сохраняем изменения без перелогинивания
                form.save()
                messages.success(request, 'Ваш профиль был успешно обновлен.')
                return redirect('dashboard')
    else:
        form = UpdateProfileForm(instance=request.user)
    
    context = {'form': form}
    return render(request, template_name, context)


@login_required
def edit_address(request):
    user = request.user

    if request.method == 'POST':
        form = AddressForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Вы можете добавить сообщение об успешном обновлении адреса
            return redirect('dashboard')
    else:
        form = AddressForm(instance=user)
    
    return render(request, 'edit_address.html', {'form': form})
