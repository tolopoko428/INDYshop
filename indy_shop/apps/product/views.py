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
    
    return redirect('product_detail', pk=product_id)



@login_required
def view_order(request):
    active_order = Orders.objects.filter(user_id=request.user, status=False).first()
    
    if active_order:
        cart_items = OrderItem.objects.filter(order_id=active_order)
    else:
        cart_items = []
    
    return render(request, 'order.html', {'cart_items': cart_items, 'active_order': active_order})



@login_required
def checkout(request):
    active_order = Orders.objects.filter(user_id=request.user, status=False).first()
    
    if active_order:
        cart_items = OrderItem.objects.filter(order_id=active_order)
        
        if request.method == 'POST':
            active_order.status = True
            active_order.save()
            return redirect('view_orders')
    else:
        cart_items = []
    
    return render(request, 'checkout.html', {'cart_items': cart_items, 'active_order': active_order})




@login_required
def view_orders(request):
    user_orders = Orders.objects.filter(user_id=request.user, status=True)
    return render(request, 'orders.html', {'user_orders': user_orders})




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
