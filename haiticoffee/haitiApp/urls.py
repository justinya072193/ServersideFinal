from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'main'
urlpatterns = [
    path('/users/address', views.address, name='address'),
    path('/users/address/<int:address_id>', views.addressByID, name='addressByID')
]
