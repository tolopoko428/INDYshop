from django.shortcuts import render, redirect, get_object_or_404
from apps.admin_panel.forms import CreateProductForm, ProductEditForm
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .models import *
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import *
from django.apps import apps
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
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)

    # Получите выбранный способ доставки из GET-параметров запроса
    selected_shipping_option_id = request.GET.get('shipping_option_id')
    selected_shipping_option = None

    if selected_shipping_option_id:
        try:
            selected_shipping_option = ShippingOption.objects.get(id=selected_shipping_option_id)
        except ShippingOption.DoesNotExist:
            pass

    # Извлеките значения total_price и другие атрибуты из корзины
    total_price = sum(cart_item.get_total_price() for cart_item in cart_items if cart_item.product.price)
    total_cost = total_price  # Изначально total_cost равен total_price без учета доставки

    if request.method == 'POST':
        form = OrderForm(request.POST, user=request.user)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user

            # Установите выбранный способ доставки в заказ
            if selected_shipping_option:
                order.shipping_option = selected_shipping_option
                shipping_cost = selected_shipping_option.price
            else:
                shipping_cost = 0

            # Обновите total_cost с учетом стоимости доставки
            total_cost = total_price + shipping_cost

            order.total_price = total_price
            order.total_cost = total_cost

            order.save()

            for cart_item in cart_items:
                order_item = OrderItem(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity
                )
                order_item.save()
            cart_items.delete()
            return redirect('success_page')
    else:
        form = OrderForm(user=request.user)

    
    if selected_shipping_option:
        shipping_cost = selected_shipping_option.price
    else:
        shipping_cost = 0

            # Обновите total_cost с учетом стоимости доставки
    total_cost = total_price + shipping_cost

    context = {
        'form': form,
        'cart_items': cart_items,
        'selected_shipping_option': selected_shipping_option,
        'total_price': total_price,
        'total_cost': total_cost,
    }
    return render(request, 'checkout.html', context)



@login_required
def views_cart(request):
    template_name = 'cart.html'
    user = request.user

    cart_items = CartItem.objects.filter(cart__user=user)

    total_price = sum(cart_item.get_total_price() for cart_item in cart_items if cart_item.product.price)

    # Передайте форму ShippingOptionForm в контекст для отображения в шаблоне
    shipping_option_form = ShippingOptionForm(request.POST or None)

    shipping_cost = 0  # По умолчанию стоимость доставки равна 0

    if request.method == 'POST':
        if shipping_option_form.is_valid():
            request.session['total_price'] = total_price
            request.session['total_cost'] = total_cost
            selected_shipping_option = shipping_option_form.cleaned_data['shipping_option']
            shipping_cost = selected_shipping_option.price
            request.session['selected_shipping_option_id'] = selected_shipping_option.id

    total_cost = total_price + shipping_cost

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'total_cost': total_cost,
        'shipping_option_form': shipping_option_form,
    }

    return render(request, template_name, context)


@receiver(post_save, sender=ShippingOption)
def update_shipping_cost(sender, instance, **kwargs):
    if instance.name == "Бесплатная стандартная":
        instance.shipping_cost = 0
    elif instance.name == "Стандартная доставка":
        instance.shipping_cost = 10.00
    elif instance.name == "Быстрая доставка":
        instance.shipping_cost = 20.00
app_config = apps.get_containing_app_config(__file__)


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

