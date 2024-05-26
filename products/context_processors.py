from .models import AddCart

def cart(request):
    cart_items = {}
    total_items = 0
    total_amount = 0

    if 'cart' in request.session:
        cart = request.session['cart']
        product_ids = [item['product_id'] for item in cart.values()]
        cart_items = AddCart.objects.filter(product_id__in=product_ids)
        total_items = sum(item['quantity'] for item in cart.values())
        total_amount = sum(item['quantity'] * item['price'] for item in cart.values())

    return {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_amount': total_amount,
    }
