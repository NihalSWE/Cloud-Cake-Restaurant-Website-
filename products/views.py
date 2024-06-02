from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views import View
from .models import Product,AddCart
from django.core.paginator import Paginator
from django.http import JsonResponse
# Create your views here.


def base(request):
    return render(request, 'products/base.html')

def navbar(request):
    return render(request, 'products/navbar.html')

def about(request):
    return render(request,'products/about.html')

def contactus(request):
    return render(request,'products/ContactUs.html')

class CakeView(View):
    def get(self, request):
        cakes = Product.objects.filter(category='C').order_by('-id')
        paginator = Paginator(cakes, 8)  # Display 4 cakes per page

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'cakes': page_obj,
        }
        return render(request, 'products/cake.html', context)


class SavoryView(View):
    def get(self, request):
        savories = Product.objects.filter(category='S').order_by('-id')
        savories_paginator = Paginator(savories, 8)    # Show 8 savories per page
        savories_page_number = request.GET.get('savories_page')
        context = {
            'savories': savories_paginator.get_page(savories_page_number),
            }
        return render(request,'products/savory.html',context)

class FrozenView(View):
    def get(self,request):
        frozens=Product.objects.filter(category='F').order_by('-id')
        frozens_paginator = Paginator(frozens, 8)    # Show 8 frozens per page
        frozens_page_number = request.GET.get('frozens_page')
        context = {
            'frozens': frozens_paginator.get_page(frozens_page_number),
            }
        return render(request,'products/frozen.html',context)


class BreadView(View):
    def get(self,request):
        breads=Product.objects.filter(category='B').order_by('-id')
        breads_paginator = Paginator(breads, 8)    # Show 8 beards per page
        breads_page_number = request.GET.get('beards_page')
        context = {
            'breads': breads_paginator.get_page(breads_page_number),
            }
        return render(request,'products/Bread&Cookies.html',context)

class ProductView(View):
     def get(self, request):
        cakes = Product.objects.filter(category='C').order_by('-id')
        savories = Product.objects.filter(category='S').order_by('-id')
        frozens = Product.objects.filter(category='F').order_by('-id')
        breads = Product.objects.filter(category='B').order_by('-id')

        cakes_paginator = Paginator(cakes, 4)    # Show 4 cakes per page
        savories_paginator = Paginator(savories, 4)    # Show 4 savories per page
        frozens_paginator = Paginator(frozens, 4)    # Show 4 frozens per page
        breads_paginator = Paginator(breads, 4)    # Show 4 breads per page

        context = {
            'cakes': cakes_paginator.get_page(1),
            'savories': savories_paginator.get_page(1),
            'frozens': frozens_paginator.get_page(1),
            'breads': breads_paginator.get_page(1),
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
    print("Cart Contents:", cart)
    
    total_amount = 0
    for item in cart.values():
        if 'discount_price' in item:
            total_amount += item['quantity'] * item['discount_price']
        else:
            total_amount += item['quantity'] * item['price']

    shipping = 70.00  # Example shipping cost
    total_with_shipping = total_amount + shipping
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            
            # Serialize cart items to JSON
            cart_items = json.dumps(list(cart.values()))
            
            order = Order(name=name, number=phone, address=address, cart_items=cart_items)
            order.save()
            
            # Clear the cart after placing the order
            request.session['cart'] = {}
            
            return redirect("order_conferm")
    else:
        form = OrderForm()

    context = {
        'cart': cart,
        'total_amount': total_amount,
        'shipping': shipping,
        'total_with_shipping': total_with_shipping,
        'form': form,
    }

    return render(request, 'products/showcart.html', context)



def order_conferm(request):
    return render(request,'products/order_conferm.html')

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