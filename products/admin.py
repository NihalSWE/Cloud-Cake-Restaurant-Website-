from django.contrib import admin
from .models import Product,AddCart,Order,Banner
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price','discount_price','detail','category', 'image']


@admin.register(AddCart)
class AddCartModelAdmin(admin.ModelAdmin):
    list_display=['id','product','quantity']


import json
@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'number', 'address', 'display_cart_items']

    def display_cart_items(self, obj):
        """
        Custom method to display cart items with details and calculate total cost
        """
        cart_items = obj.cart_items
        if cart_items:
            # Deserialize JSON string to Python object
            cart_items_list = json.loads(cart_items)
            total_cost = 0
            item_details = []
            for item in cart_items_list:
                title = item['title']
                quantity = item['quantity']
                original_price = item['price']
                discount_price = item.get('discount_price', None)
                price = discount_price if discount_price is not None else original_price
                total_item_cost = price * quantity
                item_details.append(
                    f"Item: {title}\nQuantity: {quantity}\nItem Price: Tk. {price}\n"
                )
                total_cost += total_item_cost
            
            # Adding shipping cost
            shipping_cost = 70.00
            total_cost_with_shipping = total_cost + shipping_cost
            
            # Return the concatenated string of item details and total cost
            return '\n'.join(item_details) + f'Shipping Cost: Tk. {shipping_cost}\nTotal Cost: Tk. {price} * {quantity} = Tk. {total_cost} + Tk. {shipping_cost} = Tk. {total_cost_with_shipping}'
        else:
            return 'No items'

    display_cart_items.short_description = 'Cart Items and Total Cost'  # Set column header


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'image')  # Display the ID and a preview of the image in the admin list view

    def image(self, obj):
        if obj.image:
            return f'<img src="{obj.image.url}" style="max-height: 100px; max-width: 200px;" />'
        else:
            return 'No Image'
    
    image.allow_tags = True  # Allows HTML content in the method's return value
    image.short_description = 'Image Preview'  # Sets the column header text in the admin list view