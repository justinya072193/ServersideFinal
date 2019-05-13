from django.shortcuts import render
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from rest_framework import status
from django.contrib.auth.models import User
from haitiApp.models import Address
import hashlib
import json
from django.views.decorators.csrf import csrf_exempt
from haitiApp.forms import NewAddressForm

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
        currUser = User.objects.get(id=user_id)
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