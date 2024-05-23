from django.shortcuts import render
from django.views import View
from .models import Product
from django.core.paginator import Paginator
# Create your views here.


def base(request):
    return render(request, 'products/base.html')

# def home(request):
    # return render (request,'products/home.html')

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



# class ProductView(View):
#     def get(self, request):
#         juices = Product.objects.filter(category='J')
#         cakes = Product.objects.filter(category='C')
#         burgers = Product.objects.filter(category='B')
#         pizzas = Product.objects.filter(category='P')

#         juices_paginator = Paginator(juices, 8)  # Show 8 juices per page
#         cakes_paginator = Paginator(cakes, 8)    # Show 8 cakes per page
#         burgers_paginator = Paginator(burgers, 8)  # Show 8 burgers per page
#         pizzas_paginator = Paginator(pizzas, 8)  # Show 8 pizzas per page

#         juices_page_number = request.GET.get('juices_page')
#         cakes_page_number = request.GET.get('cakes_page')
#         burgers_page_number = request.GET.get('burgers_page')
#         pizzas_page_number = request.GET.get('pizzas_page')

#         context = {
#             'juices': juices_paginator.get_page(juices_page_number),
#             'cakes': cakes_paginator.get_page(cakes_page_number),
#             'burgers': burgers_paginator.get_page(burgers_page_number),
#             'pizzas': pizzas_paginator.get_page(pizzas_page_number),
#         }
#         return render(request, 'app/home.html', context)        