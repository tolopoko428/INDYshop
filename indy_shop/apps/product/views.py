from django.shortcuts import render, redirect, get_object_or_404
from .forms import CreateProductForm
from .models import Product, ProductImage
from datetime import datetime, timedelta
# Create your views here.


def error(request):
    templates_name = '404.html'
    return render(request, templates_name)




def add_product(request):
    if request.method == 'POST':
        print(request.POST)
        form = CreateProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()  # Создайте объект Product

            # После создания продукта, создайте объекты ProductImage для изображений
            for image in request.FILES.getlist('images'):
                product_image = ProductImage(product_image_id=product, images=image, is_main=False)  # Установите is_main=False, так как это может не быть основным изображением
                product_image.save()




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

            return redirect('empty-paht')  # Перенаправьтесь на нужную страницу после успешного сохранения
    else:
        form = CreateProductForm()
    
    return render(request, 'add_product.html', {'form': form})




def all_products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products': products})



def detail_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'product_detail.html', {'product': product})



def top_edit_product(request, product_id):
    product = Product.objects.get(pk=product_id)

    if product.discount > 0:
        product.is_top = True

    product.save()