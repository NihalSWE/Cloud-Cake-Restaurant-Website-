from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views import View
from .models import Product,AddCart,Banner,CategoryImage,FoodItems,AboutUs, AboutUs_TeamMember
from django.core.paginator import Paginator
from django.http import JsonResponse

# Create your views here.


def base(request):
    return render(request, 'products/base.html')

def navbar(request):
    return render(request, 'products/navbar.html')



from .models import Outlet

def outlet(request):
    outlets = Outlet.objects.all()
    return render(request,'products/outlets.html', {'outlets': outlets})

def about(request):
    about_content = AboutUs.objects.first()  # Fetches the first entry of About
    team_members = AboutUs_TeamMember.objects.all()
    return render(request, 'products/about.html', {
        'about_content': about_content,
        'team_members': team_members
    })

def contactus(request):
    return render(request,'products/ContactUs.html')


from .models import Branch, Career,Designation

from django.contrib import messages

def career(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        message = request.POST.get('message')
        branch_id = request.POST.get('branch')
        designation_id = request.POST.get('designation')
        cv = request.FILES.get('cv')

        branch = Branch.objects.get(id=branch_id)
        designation = Designation.objects.get(id=designation_id)

        career = Career(
            name=name,
            number=number,
            email=email,
            address=address,
            message=message,
            branch=branch,
            designation=designation,
            cv=cv
        )
        career.save()
        messages.success(request, 'Your application has been submitted successfully!')
        return redirect('career') 

    branches = Branch.objects.all()
    designations = Designation.objects.all()
    return render(request, 'products/career.html', {'branches': branches, 'designations': designations})



class CakeView(View):
    def get(self, request):
        cakes = Product.objects.filter(category='C').order_by('id')
        paginator = Paginator(cakes, 5)  # Display 4 cakes per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'cakes': page_obj,
        }
        return render(request, 'products/cake.html', context)


class SavoryView(View):
    def get(self, request):
        savories = Product.objects.filter(category='S').order_by('id')
        paginator = Paginator(savories, 5)  # Display 5 savories per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'savories': page_obj,
        }
        return render(request, 'products/savory.html', context)


class FrozenView(View):
    def get(self, request):
        frozens = Product.objects.filter(category='F').order_by('id')
        paginator = Paginator(frozens, 5)  # Display 5 frozens per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'frozens': page_obj,
        }
        return render(request, 'products/frozen.html', context)


class BreadView(View):
    def get(self, request):
        breads = Product.objects.filter(category='B').order_by('id')
        paginator = Paginator(breads, 5)  # Display 5 breads per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'breads': page_obj,
        }
        return render(request, 'products/Bread&Cookies.html', context)



class ProductView(View):
    def get(self, request):
        # Get the latest banner
        latest_banner = Banner.objects.latest('id')

        # Delete all previous banners except the latest one
        Banner.objects.exclude(id=latest_banner.id).delete()

        cakes = Product.objects.filter(category='C').order_by('id')
        savories = Product.objects.filter(category='S').order_by('id')
        frozens = Product.objects.filter(category='F').order_by('id')
        breads = Product.objects.filter(category='B').order_by('id')

        cakes_paginator = Paginator(cakes, 4)    # Show 4 cakes per page
        savories_paginator = Paginator(savories, 4)    # Show 4 savories per page
        frozens_paginator = Paginator(frozens, 4)    # Show 4 frozens per page
        breads_paginator = Paginator(breads, 4)    # Show 4 breads per page

        # Fetch category images
        category_images = {ci.category: ci.image.url for ci in CategoryImage.objects.all()}

        context = {
            'banner': latest_banner,
            'cakes': cakes_paginator.get_page(1),
            'savories': savories_paginator.get_page(1),
            'frozens': frozens_paginator.get_page(1),
            'breads': breads_paginator.get_page(1),
            'category_images': category_images,
        }

        return render(request, 'products/home.html', context)


class ProductDetailView(View):
 def get(self, request, pk):
  product=Product.objects.get(pk=pk)
  context={'product':product}
  return render(request, 'products/productdetails.html',context)
 

class QuickView(View):
    def get(self, request, pk):
        product=Product.objects.get(pk=pk)
        context={'product':product}
        return render(request, 'products/quickview.html',context)



def addtocart(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    cart = request.session.get('cart', {})

    if str(prod_id) in cart:
        cart[str(prod_id)]['quantity'] += 1
    else:
        product_data = {
            'product_id': prod_id,
            'quantity': 1,
            'price': product.price,
            'title': product.title,
            'image_url': product.image.url
        }
        if product.discount_price:
            product_data['discount_price'] = product.discount_price
        cart[str(prod_id)] = product_data

    total_cart_quantity = sum(item['quantity'] for item in cart.values())
    request.session['cart'] = cart

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'total_cart_quantity': total_cart_quantity, 'cart': cart})

    return redirect('showcart')

def remove_item(request, prod_id):
    cart = request.session.get('cart', {})

    if str(prod_id) in cart:
        del cart[str(prod_id)]
        request.session['cart'] = cart

    return redirect('showcart')

def update_quantity(request, prod_id, action):
    cart = request.session.get('cart', {})

    if str(prod_id) in cart:
        if action == 'increase':
            cart[str(prod_id)]['quantity'] += 1
        elif action == 'decrease' and cart[str(prod_id)]['quantity'] > 1:
            cart[str(prod_id)]['quantity'] -= 1

        request.session['cart'] = cart

    return redirect('showcart')


import sys
import json


# Ensure the environment is using UTF-8
sys.stdout.reconfigure(encoding='utf-8')

def showcart(request):
    cart = request.session.get('cart', {})

    total_amount = 0
    for item in cart.values():
        if 'discount_price' in item:
            total_amount += item['quantity'] * item['discount_price']
        else:
            total_amount += item['quantity'] * item['price']

    # Home delivery eligibility
    home_delivery_available = total_amount > 500

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']

            cart_items = json.dumps(list(cart.values()))
            order = Order(name=name, number=phone, address=address, cart_items=cart_items)
            order.save()
            request.session['order_id'] = order.id
            request.session['cart'] = {}

            return redirect("order_conferm")
    else:
        form = OrderForm()

    context = {
        'cart': cart,
        'total_amount': total_amount,
        'form': form,
        'home_delivery_available': home_delivery_available,  # Added this
    }

    return render(request, 'products/showcart.html', context)



import json
from django.shortcuts import render, get_object_or_404
from .models import Order

def order_conferm(request):
    order_id = request.session.get('order_id')  # Get order ID from session

    if order_id:
        # Fetch the order object from the database
        order = get_object_or_404(Order, id=order_id)  
        
        # Deserialize the cart items from JSON
        cart_items = json.loads(order.cart_items)  

        # Calculate the total amount from the cart items
        total_amount = 0
        for item in cart_items:
            # Use discount_price if available, otherwise use regular price
            item_price = item.get('discount_price', item['price'])
            total_amount += item['quantity'] * item_price  # Calculate the total amount

    else:
        order = None
        cart_items = []
        total_amount = 0  # Initialize total amount as zero if no order

    context = {
        'order': order,
        'cart_items': cart_items,  # Pass cart items to the context
        'total_amount': total_amount,  # Include the total amount
    }

    return render(request, 'products/order_conferm.html', context)





from django import forms
import json

class ReadableCartItemsWidget(forms.Textarea):
    def format_value(self, value):
        if value:
            try:
                # Deserialize JSON string to Python object
                cart_items = json.loads(value)
                # Convert the list of dictionaries to a formatted string
                formatted_items = '\n'.join([f"Product: {item['title']}, Quantity: {item['quantity']}, Price: {item['price']}" for item in cart_items])
                return formatted_items
            except json.JSONDecodeError:
                return value
        return value

class OrderForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        required=True,
        label='Your Name',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        required=True,
        label='Phone Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        required=True,
        label='Address',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4})
    )
    cart_items = forms.CharField(
        widget=ReadableCartItemsWidget(),  # Use the custom widget
        required=False  # Not required because it's populated in the view
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure that cart items are properly formatted when the form is initialized
        if 'initial' in kwargs and 'cart_items' in kwargs['initial']:
            self.fields['cart_items'].initial = kwargs['initial']['cart_items']

import json

from .models import Order

def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            
            # Deserialize JSON string to Python object for cart items
            cart_items_json = form.cleaned_data['cart_items']
            cart_items = json.loads(cart_items_json)
            
            # Create and save the Order object
            order = Order(name=name, phone=phone, address=address, cart_items=cart_items)
            order.save()
            
            # Redirect to a success page or do whatever you need
            return redirect('success_page')  # Replace 'success_page' with the name of your success page URL pattern
    else:
        # Populate cart items into a JSON string and pass it to the form
        cart = request.session.get('cart', {})
        cart_items_json = json.dumps(cart)
        form = OrderForm(initial={'cart_items': cart_items_json})

    return render(request, 'products/order.html', {'form': form})

from .models import ContactMessage

def contactus(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        number = request.POST.get('number')
        email = request.POST.get('email')
        address = request.POST.get('address')
        message = request.POST.get('message')

        # Save the form data to the database
        ContactMessage.objects.create(
            name=name,
            number=number,
            email=email,
            address=address,
            message=message
        )

        # Redirect to a success page after form submission to avoid form resubmission on page reload
        return redirect('contactus')

    return render(request, 'products/contactus.html')


from django.http import JsonResponse
from .models import FoodItems

from products.models import Product  # Import the correct model

def foodmenu(request):
    # Get the filter value if it exists
    filter_value = request.GET.get('filter', '')

    if filter_value:
        # Filter items based on the search input
        products = Product.objects.filter(title__icontains=filter_value) | Product.objects.filter(price__icontains=filter_value)
    else:
        products = Product.objects.all()

    # Check if the request is an AJAX request
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        # Return filtered items as JSON for the autocomplete
        product_list = list(products.values('title'))
        return JsonResponse(product_list, safe=False)

    # Pass the products to the template
    return render(request, 'products/foodmenu.html', {'products': products})



from django.template.loader import render_to_string
from xhtml2pdf import pisa
from io import BytesIO
from .models import FoodItems

def download_food_menu(request):
    # Get the filter value from the request
    filter_value = request.GET.get('filter', '')

    if filter_value:
        # Filter items based on the search input
        items = FoodItems.objects.filter(name__icontains=filter_value) | FoodItems.objects.filter(mrp__icontains=filter_value)
    else:
        items = FoodItems.objects.all()

    # Render the HTML template with context data
    template_path = 'products/food_menu_pdf.html'
    context = {'items': items}
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="food_menu.pdf"'

    # Create a byte stream buffer
    buffer = BytesIO()

    # Render the template into a PDF
    html = render_to_string(template_path, context)
    pisa_status = pisa.CreatePDF(BytesIO(html.encode("utf-8")), dest=buffer)

    # If there's an error during PDF generation
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    # Write the PDF buffer to the response
    response.write(buffer.getvalue())
    return response


def error_page(request, exception):
    return render(request, 'products/404.html')

