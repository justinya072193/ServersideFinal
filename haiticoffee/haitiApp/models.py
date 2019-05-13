from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Address(models.Model) :
    addressLine1 = models.CharField('addressLine1', max_length=250)
    addressLine2 = models.CharField('addressLine2', max_length=250, default=None)
    city = models.CharField('city', max_length=250)
    state = models.CharField('state', max_length=30)
    postalCode = models.CharField('postalCode', max_length=10)
    country = models.CharField('country', max_length=250, default='USA')
    
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    customerAddress = models.ManyToManyField(Address)
    isAdmin = models.BooleanField('isAdmin', default=False)
    isVendor = models.BooleanField('isVendor', default=False)
    isFarmer = models.BooleanField('isFarmer', default=False)

class Order(models.Model):
    customer = models.ForeignKey('customer', Customer)
    orderDate = models.DateTimeField('orderDate', auto_now_add = True)
    status = models.TextField('status', max_length = 250, default = 'Order Received')
    totalPrice = models.TextField('totalPrice', max_length = 50)

class Cart(models.Model):
    customer = models.ForeignKey('customer', Customer)
    totalPrice = models.TextField('totalPrice', max_length = 50, default = 0)
    orderID = models.OneToOneField(Order, on_delete=models.CASCADE, default = None)



class Product(models.Model):
    productName = models.TextField('productName', max_length = 250, unique = True)
    productDescription = models.TextField('productDescription', max_length = 250)
    productPrice = models.DecimalField('productPrice', max_digits=5, decimal_places=2)
    productCart = models.ManyToManyField(Cart)
    #productOrder = models.ManyToManyField(Order)

class Product_Image(models.Model) :
    product = models.ForeignKey('product', Product)
    img = models.ImageField('img')








