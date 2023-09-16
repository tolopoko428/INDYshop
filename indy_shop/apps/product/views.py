from django.shortcuts import render, redirect, get_object_or_404
from apps.admin_panel.forms import CreateProductForm, ProductEditForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import AddToFavoritesForm
# Create your views here.


def all_products(request):
    products = Product.objects.all()
    return render(request, 'all_products.html', {'products': products})



def detail_product(request, pk):
    template_name = 'detail_product.html'
    product = get_object_or_404(Product, pk=pk)
    return render(request, template_name, {'product': product})




@login_required
def add_to_order(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    active_order = Orders.objects.filter(user_id=request.user, status=False).first()
    
    if active_order is None:
        active_order = Orders.objects.create(user_id=request.user, total_amount=0)
    
    order_item, created = OrderItem.objects.get_or_create(order_id=active_order, order_item_id=product, defaults={'quantity': 1})

    if not created:
        order_item.quantity += 1
        order_item.save()
    
    return redirect('empty-paht')



@login_required
def remove_from_order(request, product_id):
    try:
        product = Product.objects.get(pk=product_id)
        order = Orders.objects.get(user_id=request.user, status=False)
        order_item = OrderItem.objects.get(order_id=order, order_item_id=product)
        order_item.delete()
        return redirect('cart.html')
    except (Product.DoesNotExist, Orders.DoesNotExist, OrderItem.DoesNotExist):
        return render(request, 'error', {'error_message': 'Товар не найден в корзине.'})



@login_required
def view_orders(request):
    active_order = Orders.objects.filter(user_id=request.user, status=False).first()
    
    if active_order:
        cart_items = OrderItem.objects.filter(order_id=active_order)
    else:
        cart_items = []
    return render(request, 'cart.html', {'cart_items': cart_items, 'active_order': active_order})



@login_required
def cart_items(request):
    user = request.user
    order = Orders.objects.filter(user_id=user, status=False).first()

    if order:
        cart_items = order.order_items.all()
        cart_count = [item.quantity for item in cart_items]
    else:
        cart_items = []
        cart_count = 0

    context = {
        'cart_items': cart_items,
        'cart_count': cart_count,
    }

    return context




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