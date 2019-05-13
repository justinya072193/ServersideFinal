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


class Cart(models.Model):
    customer = models.ForeignKey('customer', Customer)
    totalPrice = models.DecimalField('totalPrice', max_digits = 5, decimal_places = 2)

class Order(models.Model):
    statusChoices = (
        ('UNFULFILLED', 'Unfulfilled'),
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('FULFILLED', 'Fulfilled')
    )
    customer = models.ForeignKey('customer', Customer)
    orderDate = models.DateTimeField('orderDate', auto_now_add = True)
    status = models.TextField('status', max_length = 250, default = 'Order Received')
    totalPrice = models.DecimalField('totalPrice', max_digits = 5, decimal_places = 2)
    cartID = models.ForeignKey('Cart', Cart)



class Product(models.Model):
    productName = models.TextField('productName', max_length = 250, unique = True)
    productDescription = models.TextField('productDescription', max_length = 250)
    productPrice = models.DecimalField('productPrice', max_digits=5, decimal_places=2)
    productCart = models.ManyToManyField(Cart)
    #productOrder = models.ManyToManyField(Order)

class Product_Image(models.Model) :
    product = models.ForeignKey('product', Product)
    img = models.ImageField('img')








