from django.contrib import admin
from .models import Product,AddCart,Contact
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price','category', 'image']


@admin.register(AddCart)
class AddCartModelAdmin(admin.ModelAdmin):
    list_display=['id','product','quantity']

@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display=['id','name','number','address']