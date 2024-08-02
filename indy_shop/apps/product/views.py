from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.dispatch import receiver
from .forms import *
from django.apps import apps
from ..account.views import is_logged_in
# Create your views here.


def all_products(request):
    category = request.GET.get('category')
    size = request.GET.get('size')
    color = request.GET.get('color')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.filter(status='in_stock')

    if category:
        products = products.filter(category__name=category)
    if size:
        products = products.filter(size__name=size)
    if color:
        products = products.filter(color__name=color)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    for product in products:
        # Вычислите скидку и общую цену для каждого продукта
        if product.is_top:
            product.old_price = product.price
            product.new_price = product.price - product.discount
        else:
            product.old_price = None
            product.new_price = None

    context = {
        'filtered_products': products,
    }
    return render(request, 'all_products.html', context)




def detail_product(request, pk):
    template_name = 'detail_product.html'
    product = get_object_or_404(Product, pk=pk)

    # Рассчитать старую цену на основе скидки и текущей цены
    old_price = product.price - product.discount if product.is_top else None
    new_price = product.price if product.is_top else None

    context = {
        'product': product,
        'old_price': old_price,
        'new_price': new_price,
    }
    
    return render(request, template_name, context)




@is_logged_in
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




@is_logged_in
def view_favorites(request):
    user = request.user
    favorites = FavoriteProduct.objects.filter(user_id=user)
    context = {'user': user, 'favorites': favorites}
    return render(request, 'wishlist.html', context)



@is_logged_in
def remove_favorite_list(request, pk):
    user = request.user
    product = get_object_or_404(Product, pk=pk)
    favorite_product = FavoriteProduct.objects.filter(user=user, product=product).first()
    if favorite_product:
        favorite_product.delete()
    return redirect('wishlist')



@is_logged_in
def checkout(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)

    selected_shipping_option_id = request.GET.get('shipping_option_id')
    selected_shipping_option = None

    if selected_shipping_option_id:
        try:
            selected_shipping_option = ShippingOption.objects.get(id=selected_shipping_option_id)
        except ShippingOption.DoesNotExist:
            pass

    total_price = sum(cart_item.get_total_price() for cart_item in cart_items)
    total_cost = total_price

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = user

            if not user.first_name:
                user.first_name = form.cleaned_data['first_name']
            if not user.last_name:
                user.last_name = form.cleaned_data['last_name']
            if not user.mobile:
                user.mobile = form.cleaned_data['mobile']
            if not user.address:
                user.address = form.cleaned_data['address']
            user.save()

            selected_shipping_option_id = request.POST.get("shipping_option_id")
            order.shipping_option_id = selected_shipping_option_id

            if selected_shipping_option_id is None:
                selected_shipping_option = ShippingOption.objects.get(id=7)
            else:
                selected_shipping_option = ShippingOption.objects.get(id=selected_shipping_option_id)
            
            shipping_cost = selected_shipping_option.price if selected_shipping_option else 0
            total_cost = total_price + shipping_cost

            order.total_cost = total_cost
            order.save()

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order_id=order,
                    order_item_id=cart_item.product,
                    quantity=cart_item.quantity
                )
            cart_items.delete()
            return redirect('empty-paht')

    else:
        form = OrderForm()

    if not selected_shipping_option:
        try:
            selected_shipping_option = ShippingOption.objects.get(id=7)
        except ShippingOption.DoesNotExist:
            pass

    if selected_shipping_option:
        shipping_cost = selected_shipping_option.price
    else:
        shipping_cost = 0

    total_cost = total_price + shipping_cost

    context = {
        'form': form,
        'cart_items': cart_items,
        'selected_shipping_option': selected_shipping_option,
        'total_price': total_price,
        'total_cost': total_cost,
    }

    return render(request, 'checkout.html', context)


@is_logged_in
def views_cart(request):
    template_name = 'cart.html'
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    total_price = sum(cart_item.product.price * cart_item.quantity for cart_item in cart_items)
    total_quantity = sum(cart_item.quantity for cart_item in cart_items)
    shipping_option_form = ShippingOptionForm(request.POST or None)
    shipping_cost = 0  
    total_cost = total_price 

    if request.method == 'POST':
        if shipping_option_form.is_valid():
            selected_shipping_option = shipping_option_form.cleaned_data['shipping_option']
            shipping_cost = selected_shipping_option.price
            total_cost += shipping_cost

            request.session['total_price'] = total_price
            request.session['total_cost'] = total_cost
            request.session['selected_shipping_option_id'] = selected_shipping_option.id

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'total_cost': total_cost,
        'shipping_option_form': shipping_option_form,
        'total_quantity': total_quantity,  
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


@is_logged_in
def add_to_cart(request, product_id):
    if request.method == 'POST':
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
        else:
            cart_item.quantity = quantity
        cart_item.save()

    return redirect('empty-paht')




@is_logged_in
def remove_from_cart(request, product_id):
    user = request.user
    cart = Cart.objects.get(user=user)
    product = get_object_or_404(Product, id=product_id)
    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('cart')



@is_logged_in
def clear_cart(request):
    user = request.user

    CartItem.objects.filter(cart__user=user).delete()

    return redirect('cart')





def product_search(request):
    query = request.GET.get('q')
    results = Product.objects.filter(title__icontains=query)
    return render(request, 'search_results.html', {'results': results, 'query': query})



@is_logged_in
def order_detail(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
    except Orders.DoesNotExist:
        order = None

    context = {
        'order': order,
    }

    return render(request, 'order_detail.html', context)



@is_logged_in
def order_list(request, user_id):
    user_orders = Orders.objects.filter(user_id=user_id).exclude(status='Отменен')
    context = {
        'orders': user_orders,
    }
    return render(request, 'order_list.html', context)



@is_logged_in
def cancel_order(request, order_id):
    try:
        order = Orders.objects.get(id=order_id)
        if order.status == 'Новый Заказ':
            if request.method == 'POST':
                order.status = 'Отменен'
                order.save()
                return redirect('order_list', user_id=order.user_id)
            return render(request, 'order_cancel_confirm.html', {'order': order})
        else:
            return render(request, 'order_cancel_error.html', {'order': order})
    except Orders.DoesNotExist:
        return redirect('empty-path')