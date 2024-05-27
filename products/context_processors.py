from .models import AddCart, Product

def cart_context(request):
    cart_items = []
    total_items = 0
    total_amount = 0

    session_cart = request.session.get('cart', {})
    if session_cart:
        product_ids_quantities = [(item['product_id'], item['quantity']) for item in session_cart.values()]
        # Retrieve Product objects based on product IDs
        products = Product.objects.filter(id__in=[item[0] for item in product_ids_quantities])
        # Create a dictionary mapping product IDs to their quantities
        product_quantity_dict = {item[0]: item[1] for item in product_ids_quantities}
        # Combine Product objects with their quantities
        cart_items = [{'product': product, 'quantity': product_quantity_dict[product.id]} for product in products]
        # Calculate total items and total amount
        total_items = sum(item['quantity'] for item in cart_items)
        total_amount = sum(
            item['quantity'] * (item['product'].discount_price if item['product'].discount_price else item['product'].price)
            for item in cart_items
        )

    return {
        'cart_items': cart_items,
        'total_items': total_items,
        'total_amount': total_amount,
    }