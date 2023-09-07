from django.shortcuts import render, redirect

from django.views.generic import FormView, CreateView, TemplateView
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse_lazy
from django.http import HttpResponse
# Create your views here.

from apps.account.forms import LoginForm, UserRegisterForm
from apps.account.models import User


class LoginView(FormView):
    form_class = LoginForm
    template_name ="login.html"

    def form_valid(self, form):
        data = form.cleaned_data #{"password":"admin", "email":"admin@gmail.com"}
        # cleaned_data хранилище данных из формы в виде dict
        print(data)
        email = data["email"]
        password = data["password"]
        user = authenticate(email=email,password=password)
        if user is not None:
            if user.is_active:
                login(self.request, user)
                return redirect("index")
            return HttpResponse("Ваш аккаунт не активен!")
        return HttpResponse("Введенные вами данные некорректные!")



def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index")


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
            return redirect("base.html")
    
    context = {'form':form}
    return render(request, template_name, context)



def registration_done(request):
    return render(request, 'registration_done.html')


def index(request):
    template_name = 'base.html'
    return render(request, template_name)


