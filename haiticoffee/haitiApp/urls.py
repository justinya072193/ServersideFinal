from django.contrib import admin
from django.urls import path, include
from . import views

#this creates path 
app_name = 'haitiApp'

urlpatterns = [
    path('carts', views.carts, name = "cart"),
    path('carts/<int:cart_id>', views.cartByID, name = "cartByID"),
    path('orders', views.orders, name = "orders"),
    path('orders/<int:order_id>', views.ordersByID, name = "ordersByIDS"),
    path('users/create-address', views.address, name='address'),
    path('users/address', views.addressByUser, name='addressByUser')
    path('vendors', views.vendors, name = "vendors"),
    path('vendors/<int:cust_id>', views.patchVendors, name = "vendors"),
    path('farmers', views.farmers, name = "farmers"),
    #path('vendors', views.patchVendors, name = "patchVendors")
]
