from django.shortcuts import render, redirect, get_object_or_404
from apps.admin_panel.forms import CreateProductForm, ProductEditForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
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

    cart_items = CartItem.objects.filter(cart__user=user)

    total_price = sum(cart_item.get_total_price() for cart_item in cart_items if cart_item.product.price)

    shipping_cost = 0
    if total_price >= 10:
        shipping_cost = 0
    else:
        shipping_cost = 10 if total_price < 10 else 20

    total_cost = total_price + shipping_cost

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'total_cost': total_cost,
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
def remove_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('cart')



@login_required
def clear_cart(request):
    user = request.user

    CartItem.objects.filter(cart__user=user).delete()

    return redirect('cart')





def product_search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})

