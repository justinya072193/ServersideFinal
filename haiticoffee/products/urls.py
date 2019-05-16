from django.contrib import admin
from django.urls import path, include
from . import views

#this creates path 
app_name = 'products'

urlpatterns = [
    path('create', views.createProducts, name = "createProducts"),
    path('', views.products, name="products"),
    path('<int:product_id>/manage-images', views.manageProductImages, name='manageProductImages'),
    path('<int:product_id>/images', views.getProductImages, name='getProductImages')
]
