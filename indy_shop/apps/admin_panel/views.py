from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProductForm, ProductEditForm
from apps.product.models import Product, ProductImage
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

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

            # Обработка успешного редактирования
            # Сохраняем изображения
            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            return redirect('admin')  # Замените 'admin' на ваше представление администратора
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

            # После создания продукта, создайте объекты ProductImage для изображений
            for image in request.FILES.getlist('images'):
                product_image = ProductImage(product_image_id=product, images=image, is_main=False)  # Установите is_main=False, так как это может не быть основным изображением
                product_image.save()

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