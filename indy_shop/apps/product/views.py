from django.shortcuts import render, redirect, get_object_or_404
from apps.admin_panel.forms import CreateProductForm, ProductEditForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import *
# Create your views here.


def all_products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products': products})



def detail_product(request, pk):
    template_name = 'detail_product.html'
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {'product': product})



# @login_required
# def create_order(request, product_id):
#     product = get_object_or_404(Product, id=product_id)

#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user_id = request.user
#             order.save()
#             order.products.add(product)
#             return redirect('order_list')
#     else:
#         # Передайте данные из модели пользователя в поля формы вручную
#         initial_data = {
#             'total_amount': product.price,
#             'status': 'Обработка',
#             'postal_code': None,  # Установите по умолчанию, если требуется
#         }
#         form = OrderForm(initial=initial_data)

#     return render(request, 'create_order.html', {'form': form})




@login_required
def remove_from_order(request, product_id):
    pass


@login_required
def view_orders(request):
    pass



@login_required
def add_to_favorites(request, product_id):
    user = request.user
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        form = AddToFavoritesForm(request.POST)
        if form.is_valid():
           if not FavoriteProduct.objects.filter(user_id=user.id, product_id=product.id).exists():
                favorite_product = FavoriteProduct(user_id=user.id, product_id=product.id)
                favorite_product.save()
    return redirect('wishlist')




@login_required
def view_favorites(request):
    user = request.user
    favorites = FavoriteProduct.objects.filter(user_id=user)
    context = {'user': user, 'favorites': favorites}
    return render(request, 'wishlist.html', context)



@login_required
def remove_favorite_list(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    favorite_product = FavoriteProduct.objects.filter(user=user, product=product).first()
    if favorite_product:
        favorite_product.delete()
    return redirect('wishlist')



@login_required
def views_cart(request):
    template_name = 'cart.html'
    user = request.user

    cart_items = Cart.objects.filter(user=user)

    context = {
        'cart_items': cart_items,
    }

    return render(request, template_name, context)


@login_required
def add_to_cart(request, product_id):
    if request.method == 'POST' or request.method == 'GET':
        quantity = int(request.POST.get('quantity', 1))
        user = request.user
        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)
        product = Product.objects.get(pk=product_id)

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += quantity
            cart_item.save()

    return redirect('empty-paht')



@login_required
def remove_from_cart(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')

        # Получите текущего пользователя
        user = request.user

        # Получите корзину пользователя
        cart = Cart.objects.get(user=user)

        # Удалите запись из корзины
        CartItem.objects.filter(cart=cart, product_id=product_id).delete()

    return redirect('cart')



@login_required
def clear_cart(request):
    # Получите текущего пользователя
    user = request.user

    # Получите корзину пользователя и удалите все записи
    CartItem.objects.filter(cart__user=user).delete()

    return redirect('cart')



def product_search(request):
    form = ProductSearchForm(request.GET)
    query = request.GET.get('q')

    if query:
        results = Product.objects.filter(title__icontains=query)
    else:
        results = None

    return render(request, 'search_results.html', {'results': results})