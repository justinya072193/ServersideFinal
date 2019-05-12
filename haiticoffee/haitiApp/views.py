from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response

from rest_framework import status
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Address, Customer, Order, Cart, Product, Product_Image, cart_product, Order_Product
from rest_framework import status
import json
import datetime
from django.views.decorators.debug import sensitive_post_parameters


