from django.shortcuts import render,HttpResponse,get_object_or_404,redirect
from django.views import View
from .models import Product,AddCart
from django.core.paginator import Paginator
# Create your views here.


def base(request):
    return render(request, 'products/base.html')

class CakeView(View):
    def get(self, request):
        cakes = Product.objects.filter(category='C')
        cakes_paginator = Paginator(cakes, 8)    # Show 8 cakes per page
        cakes_page_number = request.GET.get('cakes_page')
        context = {
            'cakes': cakes_paginator.get_page(cakes_page_number),
            
        }
        return render(request,'products/cake.html', context)


class SavoryView(View):
    def get(self, request):
        savories = Product.objects.filter(category='S')
        savories_paginator = Paginator(savories, 8)    # Show 8 savories per page
        savories_page_number = request.GET.get('savories_page')
        context = {
            'savories': savories_paginator.get_page(savories_page_number),
            }
        return render(request,'products/savory.html',context)

class FrozenView(View):
    def get(self,request):
        frozens=Product.objects.filter(category='F')
        frozens_paginator = Paginator(frozens, 8)    # Show 8 frozens per page
        frozens_page_number = request.GET.get('frozens_page')
        context = {
            'frozens': frozens_paginator.get_page(frozens_page_number),
            }
        return render(request,'products/frozen.html',context)


class BreadView(View):
    def get(self,request):
        breads=Product.objects.filter(category='B')
        breads_paginator = Paginator(breads, 8)    # Show 8 beards per page
        breads_page_number = request.GET.get('beards_page')
        context = {
            'breads': breads_paginator.get_page(breads_page_number),
            }
        return render(request,'products/Bread&Cookies.html',context)

class ProductView(View):
    def get(self, request):
        cakes = Product.objects.filter(category='C')
        savories = Product.objects.filter(category='S')
        frozens=Product.objects.filter(category='F')
        breads=Product.objects.filter(category='B')


        cakes_paginator = Paginator(cakes, 4)    # Show 8 cakes per page
        savories_paginator = Paginator(savories, 4)    # Show 8 savories per page
        frozens_paginator = Paginator(frozens, 4)    # Show 8 frozens per page
        breads_paginator = Paginator(breads, 4)    # Show 8 beards per page


        context = {
            'cakes': cakes_paginator.get_page(1),
            'savories': savories_paginator.get_page(1),
            'frozens': frozens_paginator.get_page(1),
            'breads': breads_paginator.get_page(1),
        }

        return render (request,'products/home.html',context)


class ProductDetailView(View):
 def get(self, request, pk):
  product=Product.objects.get(pk=pk)
  context={'product':product}
  return render(request, 'products/productdetails.html',context)



def addtocart(request, prod_id):
    product = get_object_or_404(Product, id=prod_id)
    cart = request.session.get('cart', {})

    product_data = {
        'product_id': prod_id,
        'quantity': 1,
        'price': product.price,
        'title': product.title,
        'image_url': product.image.url
    }
    
    if product.discount_price:
        product_data['discount_price'] = product.discount_price

    if str(prod_id) in cart:
        cart[str(prod_id)]['quantity'] += 1
    else:
        cart[str(prod_id)] = product_data

    request.session['cart'] = cart
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
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            
          
            return HttpResponse(f"Thank you {name}, we have received your contact details.")
    else:
        form = ContactForm()

    context = {
        'cart': cart,
        'total_amount': total_amount,
        'shipping': shipping,
        'total_with_shipping': total_with_shipping,
        'form': form,
    }

    return render(request, 'products/showcart.html', context)



def order(request):
    return render(request,'products/order.html')

from django import forms

class ContactForm(forms.Form):
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

def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Process the data in form.cleaned_data
            name = form.cleaned_data['name']
            phone = form.cleaned_data['phone']
            address = form.cleaned_data['address']
            
            # Here you can handle the data, e.g., save it to the database, send an email, etc.
            
            return HttpResponse(f"Thank you {name}, we have received your contact details.")
    else:
        form = ContactForm()

    return render(request, 'products/contact.html', {'form': form})