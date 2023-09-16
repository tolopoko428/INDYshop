from .models import Orders

def cart_items(request):
    user = request.user
    if not user.is_authenticated:
        cart_count = 0
        return {'cart_count': cart_count}
    
    order = Orders.objects.filter(user_id=user, status=False).first()

    if order:
        cart_items = order.order_items.all()
        cart_count = sum(item.quantity for item in cart_items)
    else:
        cart_count = 0

    return {'cart_count': cart_count}