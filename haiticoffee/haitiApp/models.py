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
    statusChoices = (
        ('UNFULFILLED', 'Unfulfilled'),
        ('PENDING_PAYMENT', 'Pending Payment'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
        ('FULFILLED', 'Fulfilled')
    )
    customer = models.ForeignKey('customer', Customer)
    orderDate = models.DateTimeField('orderDate', auto_now_add = True)
    status = models.CharField(choices=statusChoices, default='UNFULFILLED')
    totalPrice = models.DecimalField('productPrice', max_digits=5, decimal_places=2)
    address = models.TextField('address')

class Cart(models.Model):
    customer = models.ForeignKey('customer', Customer)
    totalPrice = models.DecimalField('productPrice', max_digits=5, decimal_places=2)
    quantity = models.IntegerField('quantity')

class Product(models.Model):
    productName = models.TextField('productName', max_length = 250)
    productDescription = models.TextField('productDescription', max_length = 250)
    productPrice = models.DecimalField('productPrice', max_digits=5, decimal_places=2)

class Product_Image(models.Model) :
    product = models.ForeignKey('product', Product)
    img = models.ImageField('img')

class cart_product(models.Model):
    cartID = models.ForeignKey(Cart, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)

class Order_Product(models.Model):
    orderID = models.ForeignKey(Order, on_delete=models.CASCADE)
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField('quantity')



