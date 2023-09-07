from django.shortcuts import render, redirect
from .forms import CreateProductForm
from .models import Product, ProductImage
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

            return redirect('empty-paht')  # Перенаправьтесь на нужную страницу после успешного сохранения
    else:
        form = CreateProductForm()
    
    return render(request, 'add_product.html', {'form': form})



def all_products(request):
    products = Product.objects.all()
    return render(request, 'category-boxed.html', {'products': products})


