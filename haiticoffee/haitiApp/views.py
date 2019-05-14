from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from haitiApp.models import Address
from django.db import DatabaseError
from .models import Address, Customer, Order, Cart, Product, Product_Image
import json
import datetime
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
import hashlib
from haitiApp.forms import NewAddressForm

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
DatabaseErrorMessage = "Error interacting with database."

# Create your views here.
@csrf_exempt
def address(request):
    """
    On GET- returns form to create an address.
    On POST- creates new address for current user.
    """
    if request.method == 'GET':
        return HttpResponse(render(request, "auth/register.html", {'form' : NewAddressForm}), status = 200) 
    elif request.method == 'POST':
        addressData = json.loads(request.body.decode('utf-8'))
        newAddress = Address(addressLine1 = addressData['addressLine1'],
                            addressLine2 = addressData['addressLine2'],
                            city = addressData['city'],
                            state = addressData['state'],
                            postalCode = addressData['postalCode'],
                            country = addressData['country'])
        newAddress.save()
        currUser = User.objects.get(id=request.user.user_id)
        currUser.customerAddress(newAddress)
        return HttpResponse('Address created successfully', status=status.HTTP_200_OK)

@csrf_exempt
def addressByID(request, address_id):
    """
    On GET- return current user's address by id
    On PATCH- Updates given address details with data provided by user.
    On DELETE- Deletes given address from user profile
    """
    if request.method == 'GET':
        currAddress = Address.objects.get(id=address_id)
        JsonResponse(currAddress, status=status.HTTP_200_OK, safe=False)
    elif request.method == 'PATCH':
        addressData = json.loads(request.body.decode('utf-8'))
        currAddress = Address.objects.get(id=address_id)
        currAddress.update(addressLine1 = addressData['addressLine1'],
                           addressLine2 = addressData['addressLine2'],
                           city = addressData['city'],
                           State = addressData['state'],
                           postalCode = addressData['postalCode'],
                           country = addressData['country'])
        return JsonResponse(currAddress, status=status.HTTP_200_OK, safe=False)
    elif request.method == 'DELETE':
        Address.objects.get(id=address_id).delete()
        return HttpResponse('Deleted address successfully.', status=status.HTTP_200_OK)

@csrf_exempt
@sensitive_post_parameters()
def carts(request):
    if(request.user.is_authenticated):
        #get all list of carts
        if(request.method == "GET"):
            carts = Cart.objects.all().values()
            cartList = list(carts)
            return JsonResponse(cartList, safe=False, status = status.HTTP_200_OK)
        #Post a new cart with total Price of 0
        elif(request.method == "POST"):
            customer = Customer.objects.get(user = request.user)
            newCart = Cart.objects.create(customer = customer, totalPrice = 0)
            newCart.save()
            cartJSON = Cart.objects.all().values().filter(pk = newCart.pk)[0]
            return JsonResponse(cartJSON, safe = False, status = status.HTTP_201_CREATED)
        else:
            return HttpResponse("Method not allowed on /messaging/channels/.", status=405)
    else:
        return HttpResponse("Unauthroized", status = 401)

def cartByID(request, cart_id):
    if(request.user.is_authenticated):
        #gets specific cart with the cartID 
        if(request.method == "GET"):
            carts = Cart.objects.all().values().filter(id = cart_id)
            cartList = list(carts)
            return JsonResponse(cartList, safe=False, status = status.HTTP_200_OK)
        #patch the cart item and updates the total price
        elif(request.method == "PATCH"):
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return HttpResponse(JSONDecodeFailMessage, status=400)
            #user must define method Add or DELETE for patch
            #user must define product name 
            try:
                productName = data['name']
                getProduct = Product.objects.values().filter(productName = productName)
                grabCart = Cart.objects.values().filter(id = cart_id)
                #user can either add or delete the product from the cart
                if (data['method'] == 'ADD'):
                    grabCart.update(totalPrice = grabCart.totalPrice + getProduct.productPrice)
                elif (data['method'] == "DELETE"):
                    grabCart.update(totalPrice = grabCart.totalPrice - getProduct.productPrice)
                cartJSON = Cart.objects.all().values().filter(id = cart_id)[0]
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
            return JsonResponse(cartJSON, safe = False, content_type = 'application/json', status = status.HTTP_202_ACCEPTED)
        #delete the cart using cartID
        elif(request.method == "DELETE"):
            grabCart = Cart.objects.filter(id = cart_id).delete()
            return HttpResponse("Delete Successful", status = 200)
        else:
            return HttpResponse("Method not allowed on /messaging/channels/.", status=405)
    else:
        return HttpResponse("Unauthroized", status = 401)
    

@csrf_exempt
@sensitive_post_parameters()
def orders(request):
    if(request.user.is_authenticated):
        #get all list of orders
        if(request.method == "GET"):
            orders = Order.objects.all().values()
            orderList = list(orders)
            return JsonResponse(orderList, safe=False, status = status.HTTP_200_OK)
        #post a new order 
        elif(request.method == "POST"):
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return HttpResponse(JSONDecodeFailMessage, status=400)
            #user must provide cartID to define total price

            try:
                cart_id = data['cartID']
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status = 400)
            totalPrice = Cart.objects.values('totalPrice').filter(id = cart_id)

            grabCart = Cart.objects.values().filter(id = cart_id)
            customer = Customer.objects.get(user = request.user)

            newOrder = Order.objects.create(customer = customer, cartID = Cart.objects.get(id = cart_id))
            newOrder.save()
            orderJSON = Order.objects.all().values().filter(pk = newOrder.pk)[0]
            return JsonResponse(orderJSON, safe = False, content_type = 'application/json', status = status.HTTP_201_CREATED)
        else:
            return HttpResponse("Method not allowed on /messaging/channels/.", status=405)
    else:
        return HttpResponse("Unauthroized", status = 401)

@csrf_exempt
@sensitive_post_parameters()
def ordersByID(request, order_id):
    if(request.user.is_authenticated):
        #get the order with specific order id
        if(request.method == "GET"):
            orders = Order.objects.all().values().filter(id = order_id)
            orderList = list(orders)
            return JsonResponse(orderList, safe=False, status = status.HTTP_200_OK)
        #update the specific order status
        elif(request.method == "PATCH"):
            #patching status only
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return HttpResponse(JSONDecodeFailMessage, status=400)
            #need new status and orderID to patch
            try:
                updatedStatus = data['status'] 
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
            getOrder = Order.objects.values().filter(id = order_id)
            getOrder.update(status = updatedStatus)
            orderJSON = Order.objects.all().values().filter(id = order_id)[0]
            return JsonResponse(orderJSON, safe = False, content_type = 'application/json', status = status.HTTP_202_ACCEPTED)
        #delete the order with orderID
        elif(request.method == "DELETE"):
            grabOrder = Order.objects.filter(id = order_id).delete()
            return HttpResponse("Delete Successful", status = 200)
        else:
            return HttpResponse("Method not allowed on /messaging/channels/.", status=405)
    else:
        return HttpResponse("Unauthroized", status = 401)


@csrf_exempt
@sensitive_post_parameters()
def vendors(request):
    if(request.user.is_authenticated):
        #gets all list of vendors
        if(request.method == "GET"):
            Vendors = Customer.objects.values().filter(isVendor = True)
            vendorList = list(Vendors)
            return JsonResponse(vendorList, safe=False, status = status.HTTP_200_OK)
        else:
            return HttpResponse("Method not allowed on /messaging/channels/.", status=405)
    else:
        return HttpResponse("Unauthroized", status = 401)

@csrf_exempt
@sensitive_post_parameters()
def patchVendors(request, cust_id):
    if(request.user.is_authenticated):
        #get specific vendor
        if(request.method == "GET"):
            Vendors = Customer.objects.values().filter(id = cust_id, isVendor = True)
            vendorList = list(Vendors)
            return JsonResponse(vendorList, safe=False, status = status.HTTP_200_OK)
        elif(request.method == "PATCH"):
            #update status of specific customer
            try:
                data = json.loads(request.body.decode('utf-8'))
            except json.JSONDecodeError:
                return HttpResponse(JSONDecodeFailMessage, status=400)
            grabCustomer = Customer.objects.values().filter(id = cust_id)

            try:
                grabCustomer.update(isVendor = data['vendor'])
            except DatabaseError:
                return HttpResponse(DatabaseErrorMessage, status=400)
            customerJSON = Customer.objects.all().values().filter(id = cust_id)[0]
            return JsonResponse(customerJSON, safe = False, content_type = 'application/json', status = status.HTTP_202_ACCEPTED)
        elif(request.method == "DELETE"):
            #delete vendor
            grabCustomer = Customer.objects.filter(id = cust_id, isVendor = True)
            grabCustomer.delete()
            return HttpResponse("Delete Successful", status = 200)
        else:
            return HttpResponse("Method not allowed on /messaging/channels/.", status=405)
    else:
        return HttpResponse("Unauthroized", status = 401)

@csrf_exempt
@sensitive_post_parameters()
def farmers(request):
    if(request.user.is_authenticated):
        #get all farmers
        if(request.method == "GET"):
            farmers = Customer.objects.values().filter(isFarmer = True)
            farmersList = list(farmers)
            return JsonResponse(farmersList, safe=False, status = status.HTTP_200_OK)
    else:
        return HttpResponse("Unauthroized", status = 401)
