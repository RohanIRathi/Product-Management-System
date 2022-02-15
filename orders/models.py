from django.db import models
from home.models import User
from products.models import Product

# Create your models here.

class Order(models.Model):
    DistributorId = models.ForeignKey(User, related_name='distributor', verbose_name='Distributor', on_delete=models.RESTRICT)
    RetailerId = models.ForeignKey(User, related_name='retailer', verbose_name='Retailer', on_delete=models.RESTRICT)
    TotalQuantity = models.SmallIntegerField(verbose_name='Total Quantity', null=False, default=0)
    TotalAmount = models.DecimalField(verbose_name='Total Amount', max_digits=10, decimal_places=2, null=False, default=0.00)
    CreationDate = models.DateTimeField(verbose_name='Order Date', auto_now_add=True)
    PaymentDate = models.DateTimeField(verbose_name='Order Payment Date')
    Products = models.ManyToManyField(Product, related_name='products', through='OrderProduct')
    
    def __str__(self):
        return str(self.CreationDate) + "_" + str(self.RetailerId.first_name)

class OrderProduct(models.Model):
    Order = models.ForeignKey(Order, related_name='order_products', on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, related_name='order_products', on_delete=models.RESTRICT)
    Discount = models.DecimalField(verbose_name='Discount', max_digits=5, decimal_places=2, null=True, blank=True)
    Quantity = models.SmallIntegerField(verbose_name='Quantity', null=False, blank=False)
    
    def __str__(self):
        return str(self.Order) + " | " + str(self.Product)