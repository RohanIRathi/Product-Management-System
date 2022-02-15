from django.db import models
from home.models import User

# Create your models here.

class Order(models.Model):
    DistributorId = models.ForeignKey(User, related_name='distributor', verbose_name='Distributor', on_delete=models.CASCADE)
    RetailerId = models.ForeignKey(User, related_name='retailer', verbose_name='Retailer', on_delete=models.CASCADE)
    TotalQuantity = models.SmallIntegerField(verbose_name='Total Quantity', null=False, default=0)
    TotalAmount = models.DecimalField(verbose_name='Total Amount', max_digits=10, decimal_places=2, null=False, default=0.00)
    CreationDate = models.DateTimeField(verbose_name='Order Date', auto_now_add=True)
    PaymentDate = models.DateTimeField(verbose_name='Order Payment Date')
    
    def __str__(self):
        return str(self.CreationDate) + "_" + str(self.RetailerId.first_name)
