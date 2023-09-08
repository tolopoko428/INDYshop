from django.shortcuts import render, redirect

from django.views.generic import FormView, CreateView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.http import HttpResponse
# Create your views here.

from apps.account.forms import LoginForm, UserRegisterForm
from apps.account.models import User
from django.contrib.auth.decorators import login_required


class LoginView(FormView):
    form_class = LoginForm
    template_name = "login.html"

    def form_valid(self, form):
        data = form.cleaned_data
        email = data["email"]
        password = data["password"]
        user = authenticate(self.request, email=email, password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("empty-paht")  # Используйте более понятное имя для страницы после входа
            return HttpResponse("Ваш аккаунт не активен!")
        return HttpResponse("Введенные вами данные некорректные!")


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("empty-paht")



def register_user(request):
    template_name = "registration.html"  
    form = UserRegisterForm()
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("login")  

    context = {"form": form}
    return render(request, template_name, context)


def index(request):
    template_name = 'base.html'
    return render(request, template_name)



@login_required
def dashboard(request):
    template_name = 'dashboard.html'
    return render(request, template_name)
        

