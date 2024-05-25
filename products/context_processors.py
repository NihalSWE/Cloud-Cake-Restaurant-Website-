from .models import AddCart

def cart(request):
    cart_items = {}
    total_items = 0
    total_amount = 0

    if 'cart' in request.session:
        cart = request.session['cart']
        cart_item_ids = cart.keys()
        cart_items = AddCart.objects.filter(id__in=cart_item_ids)
        total_items = sum(item.quantity for item in cart_items)
        total_amount = sum(item.quantity * item.product.price for item in cart_items)

    return {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_amount': total_amount,
    }