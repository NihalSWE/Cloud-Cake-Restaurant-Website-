from . import views
from django.urls import path

urlpatterns = [
    # path('',views.base,name="base"),
    
    # path ('',views.home,name="home"),

    path('',views.ProductView.as_view(),name="home"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(), name='product-detail'),

    path("cake/",views.CakeView.as_view(),name="cake"),
    path('savory/',views.SavoryView.as_view(),name="savory"),
    path('frozen/',views.FrozenView.as_view(),name="frozen"),
    path('bread/',views.BreadView.as_view(),name="bread"),


    path('addtocart/<int:prod_id>/', views.addtocart, name='addtocart'),
    path('remove_item/<int:prod_id>/', views.remove_item, name='remove_item'),
    path('update_quantity/<int:prod_id>/<str:action>/', views.update_quantity, name='update_quantity'),
    path('showcart/', views.showcart, name='showcart'),


    path('order_view/',views.order_view,name="order_view"),
    path('order_conferm/',views.order_conferm,name="order_conferm")
]