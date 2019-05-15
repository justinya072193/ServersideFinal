from django.shortcuts import render
from haitiApp.models import Product, Product_Image, Customer
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db import DatabaseError
from products.forms import NewProductForm, AddImageForm
from django.contrib.auth.decorators import login_required

JSONDecodeFailMessage = "Error decoding JSON body. Please ensure your JSON file is valid."
BadRequestMessage = "Bad request."
DatabaseErrorMessage = "Error interacting with database."

# Create your views here.
@csrf_exempt
@login_required(login_url='/auth/signin')
def createProducts(request):
    """
    On GET- returns form to create new product
    On POST- creates a new product with form input.
    On PATCH- changes specified product details with data given by user.
    On DELETE- deletes product given by user.
    """
    try :
        if not Customer.objects.get(user=request.user).isAdmin:
            return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        if request.method == "GET" :
            return HttpResponse(render(request, "products/create-a-product.html", 
                                {'form' : NewProductForm}), status = 200)
        elif request.method == "POST":
            productData = request.POST
            productImage = request.FILES
            newProduct = Product(
                productName = productData['productName'],
                productDescription = productData['productDescription'],
                productPrice = productData['productPrice']
            )
            newProduct.save()
            if productImage:
                addImageToProduct(productImage['productImage'], newProduct)
            return HttpResponse('Product created successfully', status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@login_required(login_url='/auth/signin')
def products(request):
    try:
        if request.method == "GET":
            productObjs = Product.objects.all().values()
            productList = list(productObjs)
            for product in productList:
                productObj = Product.objects.get(id=product['id'])
                product['productImages'] = list(Product_Image.objects.filter(product=productObj).values())
            return JsonResponse(productList, safe=False, status=status.HTTP_200_OK)
        elif request.method == "PATCH":
            if not Customer.objects.get(user=request.user).isAdmin:
                return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
            productData = json.loads(request.body.decode('utf-8'))
            currProduct = Product.objects.get(id=productData['id'])
            currProduct.productName = productData['productName']
            currProduct.productDescription = productData['productDescription']
            currProduct.productPrice = productData['productPrice']
            currProduct.save()
            
            productObj = Product.objects.filter(id=currProduct.id)
            productList = list(productObj.values())
            productList[0]['productImages'] = list(Product_Image.objects.filter(product=productObj[0]).values())
            return JsonResponse(productList[0], status=status.HTTP_200_OK, safe=False)
        elif request.method == "DELETE":
            if not Customer.objects.get(user=request.user).isAdmin:
                return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
            productID = json.loads(request.body.decode('utf-8'))
            productToDelete = Product.objects.get(id=productID['id'])
            relatedImages = Product_Image.objects.filter(product=productToDelete).delete()
            print(productToDelete)
            productToDelete.delete()
            return HttpResponse('Deleted product and related images successfully.', status=status.HTTP_200_OK)
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@login_required
def manageProductImages(request, product_id):
    try:
        if not Customer.objects.get(user=request.user).isAdmin:
            return HttpResponse('Must be admin to access.', status=status.HTTP_403_FORBIDDEN)
        currProduct = Product.objects.get(id=product_id)
        if request.method == "GET":
            return HttpResponse(render(request, "products/add-an-image.html", 
                            {'form' : AddImageForm}), status = 200)
        elif request.method == "POST":
            addImageToProduct(request.FILES['newImage'], currProduct)
            return HttpResponse('Added image to product', status=status.HTTP_200_OK)
        elif request.method == "DELETE":
            imageData = json.loads(request.body.decode('utf-8'))
            Product_Image.objects.get(id=imageData['id']).delete()
            return HttpResponse('Deleted Image successfully')
    except json.JSONDecodeError :
        return HttpResponse(JSONDecodeFailMessage, status=status.HTTP_400_BAD_REQUEST)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def getProductImages(request, product_id):
    try:
        currProduct = Product.objects.get(id=product_id)
        if request.method == "GET":
            images = Product_Image.objects.filter(product=currProduct).values()
            images = list(images)
            return JsonResponse(images, safe=False, status=status.HTTP_200_OK)
    except DatabaseError :
        return HttpResponse(DatabaseErrorMessage, status=status.HTTP_400_BAD_REQUEST)
    except Exception :
        return HttpResponse(BadRequestMessage, status=status.HTTP_400_BAD_REQUEST)


def addImageToProduct(imageData, product):
    newImage = Product_Image(
        product = product,
        img = imageData
    )
    newImage.save()