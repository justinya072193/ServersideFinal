from django.contrib import admin
from django.urls import path, include
from . import views

#this creates path 
app_name = 'haitiApp'

urlpatterns = [
    path('carts', views.carts, name = "cart"),
    path('carts', views.cartByID, name = "cartByID"),
    path('orders', views.orders, name = "orders"),
    path('orders', views.ordersByID, name = "ordersByIDS"),
    path('users/create-address', views.address, name='address'),
    path('users/address', views.addressByUser, name='addressByUser')
]
