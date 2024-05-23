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
]