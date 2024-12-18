from . import views
from django.urls import path
from .views import contactus

urlpatterns = [

    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),
    path('quick-view/<int:pk>', views.QuickView.as_view(), name='quick-view'),

    path('about/',views.about,name="about"),
    path('contactus/',contactus,name="contactus"),
    path('outlet/',views.outlet,name="outlet"),
    path('career/',views.career,name="career"),

    path("cake/",views.CakeView.as_view(),name="cake"),
    path('savory/',views.SavoryView.as_view(),name="savory"),
    path('frozen/',views.FrozenView.as_view(),name="frozen"),
    path('bread/',views.BreadView.as_view(),name="bread"),


    path('addtocart/<int:prod_id>/', views.addtocart, name='addtocart'),
    path('remove_item/<int:prod_id>/', views.remove_item, name='remove_item'),
    path('update_quantity/<int:prod_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('showcart/', views.showcart, name='showcart'),


    path('order_view/',views.order_view,name="order_view"),
    path('order_conferm/',views.order_conferm,name="order_conferm"),

    path('foodmenu/',views.foodmenu,name="foodmenu"),
    path('download_food_menu/', views.download_food_menu, name='download_food_menu'),

    
]