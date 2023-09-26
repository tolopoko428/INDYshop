from .models import *
from django.shortcuts import render, redirect, get_object_or_404


def cart_items(request):
    user = request.user
    cart_count = 0
    
    if user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=user)
        cart_count = sum(item.quantity for item in cart_items)

    return {'cart_count': cart_count}
