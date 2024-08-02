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
            product = form.save(commit=False)

            images = request.FILES.getlist('image')
            for image in images:
                ProductImage.objects.create(product=product, image=image)

            discount = form.cleaned_data.get('discount')
            if discount is None or discount == 0:
                discount = 0

            product.price -= discount
            if discount > 0:
                product.is_top = True
            else:
                product.is_top = False
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
            product = form.save() 
            today = datetime.now().date()
            one_week_ago = today - timedelta(days=7)
            
            if product.created_at.date() >= one_week_ago:
                product.is_new = True
            product.save()

            images = request.FILES.getlist('images')
            is_main = True 
            for image_form in images:
                product_image = ProductImage(product=product, image=image_form, is_main=is_main)
                product_image.save()
                is_main = False

            return redirect('admin')
    else:
        form = CreateProductForm()
    
    return render(request, 'add_product.html', {'form': form})



@user_passes_test(is_personal, login_url='error')
def admin_ponel(request):
    template_name = 'admin.html'
    products =  Product.objects.all()
    for product in products:
        if product.is_top:
            product.old_price = product.price
            product.new_price = product.price - product.discount
        else:
            product.old_price = None
            product.new_price = None
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




@user_passes_test(is_personal, login_url='error')
def admin_update_order_status(request, order_id):
    try:
        order = get_object_or_404(Orders, id=order_id)

        status_transitions = {
            'Новый Заказ': 'Обработка',
            'Обработка': 'В Пути',
            'В Пути': 'Доставлено',
        }

        current_status = order.status
        if current_status in status_transitions:
            next_status = status_transitions[current_status]
            order.status = next_status
            order.save()

        return redirect('admin_order_list')
    except Orders.DoesNotExist:
        return redirect('empty-path')

    

@user_passes_test(is_personal, login_url='error')
def admin_order_list(request):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    product_name = cart_items[0].product.title if cart_items else None

    try:
        # Получаем все заказы
        orders = Orders.objects.all()

        # Фильтруем заказы по статусам "Доставлено" и "Отменен"
        delivered_orders = orders.filter(status='Доставлено')
        cancelled_orders = orders.filter(status='Отменен')
        # Оставляем только заказы, которые не "Доставлено" и не "Отменен"
        pending_orders = orders.exclude(status__in=['Доставлено', 'Отменен'])

        context = {
            'product_name': product_name,
            'delivered_orders': delivered_orders,
            'cancelled_orders': cancelled_orders,
            'pending_orders': pending_orders,
        }
        return render(request, 'admin_order_list.html', context)
    except Orders.DoesNotExist:
        return redirect('empty-path')





@user_passes_test(is_personal, login_url='error')
def user_profile(request, user_id):
    user = request.user
    cart_items = CartItem.objects.filter(cart__user=user)
    product_name = cart_items[0].product.title if cart_items else None
    user = get_object_or_404(User, id=user_id)
    orders = user.orders.all()
    
    context = {
        'user': user,
        'orders': orders,
        'product_name':product_name,
    }
    return render(request, 'admin_user_profile.html', context)



@user_passes_test(is_personal, login_url='error')
def status_update(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if product.status == 'in_stock':
        product.status = 'out_of_stock'
    else:
        product.status = 'in_stock'
    
    product.save()

    return redirect('admin')


@user_passes_test(is_personal, login_url='error')
def not_active_products(request):
    out_of_stock_products = Product.objects.filter(status='out_of_stock')
    for product in out_of_stock_products:
        # Вычислите скидку и общую цену для каждого продукта
        if product.is_top:
            product.old_price = product.price
            product.new_price = product.price - product.discount
        else:
            product.old_price = None
            product.new_price = None
            
    context = {
        'out_of_stock_products': out_of_stock_products
    }
    return render(request, 'not_active_products.html', context)



@user_passes_test(is_personal, login_url='error')
def detail_order_user(request, product_id, user_id):
    # Получаем пользователя и заказ на основе user_id и product_id
    user = get_object_or_404(User, id=user_id)
    order = get_object_or_404(Orders, user=user, id=product_id)

    # Получите список заказов пользователя "Вель"
    orders = Orders.objects.filter(user=user)

    # Получите все элементы заказа для данного заказа
    order_items = OrderItem.objects.filter(order_id=order)

    # Создайте список продуктов в данном заказе
    products_in_order = [item.order_item_id for item in order_items]

    # Добавьте postal_code и orders_text в контекст
    postal_code = order.postal_code
    orders_text = order.orders_text

    # Добавьте update_dates в контекст
    context = {
        'user': user,
        'order': order,
        'orders': orders,  # Передаем список заказов
        'products_in_order': products_in_order,  # Передаем список продуктов в данном заказе
        'postal_code': postal_code,  # Передаем postal_code
        'orders_text': orders_text,  # Передаем orders_text
    }

    return render(request, 'order_detail.html', context)
