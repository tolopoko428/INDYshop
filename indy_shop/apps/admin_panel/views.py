from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from apps.product.models import Product, ProductImage
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

def error(request):
    templates_name = '404.html'
    return render(request, templates_name)



def is_personal(user):
    return user.is_staff or user.is_superuser



def is_superuser(user):
    return user.is_superuser



@user_passes_test(is_personal, login_url='error')
def update_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = ProductEditForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()

            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            discount = form.cleaned_data.get('discount')
            if discount == 0 or discount == None:
                pass
            elif discount < 1:
                product.price -= discount
                product.is_top = True
                product.save()

            return redirect('admin')
    else:
        form = ProductEditForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})




@user_passes_test(is_personal, login_url='error')
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('admin')


    
@user_passes_test(is_personal, login_url='error')
def add_product(request):
    if request.method == 'POST':
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # Создайте объект Product

            # Проверяем, был ли продукт добавлен в течение недели
            today = datetime.now().date()
            one_week_ago = today - timedelta(days=7)
            
            if product.created_at.date() >= one_week_ago:
                product.is_new = True  # Устанавливаем метку "New" 

            product.save()

            images = request.FILES.getlist('images')
            is_main = True  # Устанавливаем флаг is_main для первого изображения
            for image_form in images:
                product_image = ProductImage(product=product, image=image_form, is_main=is_main)
                product_image.save()
                is_main = False

            return redirect('admin')  # Перенаправьтесь на нужную страницу после успешного сохранения
    else:
        form = CreateProductForm()
    
    return render(request, 'add_product.html', {'form': form})



@user_passes_test(is_personal, login_url='error')
def admin_ponel(request):
    template_name = 'admin.html'
    products =  Product.objects.all()
    return render(request, template_name, {'products': products})



@user_passes_test(is_personal, login_url='error')
def admin_detail_post(request, pk):
    template_name = 'admin_detail_product.html'
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {'product': product})



@user_passes_test(is_superuser, login_url='error')
def staff_registration(request):
    template_name = 'staff_registration.html'
    form = StaffRegistrationForm()
    if request.method == "POST":
        form = StaffRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            password = form.cleaned_data["password1"]
            user = User.objects.create(
                email=form.cleaned_data["email"],
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                is_staff=True, 
            )
            user.set_password(password)
            user.save()
            return redirect("admin")
    
    context = {'form': form}
    return render(request, template_name, context)