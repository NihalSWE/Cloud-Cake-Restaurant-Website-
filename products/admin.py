from django.contrib import admin
from .models import Product,AddCart,Order,Banner,Outlet,Branch, Career
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price', 'discount_price', 'detail', 'category', 'image']
    search_fields = ['title', 'price', 'category']


@admin.register(AddCart)
class AddCartModelAdmin(admin.ModelAdmin):
    list_display=['id','product','quantity']


import json
from import_export.admin import ExportMixin
from import_export import resources, fields
# Define a resource class for the Order model
class OrderResource(resources.ModelResource):
    created_at = fields.Field(attribute='created_at', column_name='Created At')
    updated_at = fields.Field(attribute='updated_at', column_name='Updated At')

    class Meta:
        model = Order
        fields = ('id', 'name', 'number', 'address', 'created_at', 'updated_at', 'cart_items')
        export_order = ('id', 'name', 'number', 'address', 'created_at', 'updated_at', 'cart_items')

# Register your models with the admin site using the resource class
@admin.register(Order)
class OrderModelAdmin(ExportMixin, admin.ModelAdmin):
    resource_class = OrderResource
    list_display = ['id', 'name', 'number', 'address', 'display_cart_items', 'created_at', 'updated_at']
    search_fields = ['name', 'number', 'address']

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
            
            # Return the concatenated string of item details and total cost
            return '\n'.join(item_details) + f'\nTotal Cost: Tk. {total_cost}'
        else:
            return 'No items'

    display_cart_items.short_description = 'Cart Items and Total Cost'  # Set column header@admin.register(Banner)

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


from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'email', 'address', 'message', 'timestamp')
    search_fields = ['name', 'number', 'address']



@admin.register(Outlet)
class OutletAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'address', 'phone_number')


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display=('id','name')


from .models import Designation

@admin.register(Designation)
class DesignationAdmin(admin.ModelAdmin):
    list_display = ('name',)



from django.utils.html import format_html
from django.utils.http import urlencode
@admin.register(Career)
class CareerAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'email', 'address', 'branch', 'designation', 'cv_link', 'submitted_at')
    readonly_fields = ('cv_link',)

    def cv_link(self, obj):
        if obj.cv:
            cv_filename = obj.cv.name.split('/')[-1]
            if len(cv_filename) > 30:
                cv_filename = '{}...'.format(cv_filename[:27])
            return format_html('<a href="{}" download>{}</a>', obj.cv.url, cv_filename)
        return "No CV"

    cv_link.short_description = 'CV'
