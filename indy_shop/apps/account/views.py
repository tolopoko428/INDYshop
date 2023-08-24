from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Дополнительные действия после успешной регистрации
            return redirect('login')  # Перенаправление на страницу входа
    else:
        form = UserRegisterForm()
    return render(request, 'login.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Дополнительные действия после успешного входа
            return redirect('index.html')  # Перенаправление на домашнюю страницу
        else:
            # Обработка неверных данных входа
            return render(request, 'login.html', {'error_message': 'Invalid login credentials'})
    return render(request, 'login.html')


def index(request):
    template_name = 'base.html'
    return render(request, template_name)

        


    


