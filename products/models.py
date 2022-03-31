from django.db import models

# Create your models here.
class Product(models.Model):
    Company = models.CharField(verbose_name='Company', max_length=50, blank=False, null=False)
    Series = models.CharField(verbose_name='Series', max_length=50, blank=False, null=False)
    Model = models.CharField(verbose_name='Model', max_length=50, blank=False, null=False)
    Price = models.DecimalField(verbose_name='Price of the Model', max_digits=8, decimal_places=2, null=False, default=0.00)
    Quantity = models.SmallIntegerField(verbose_name='Available Quantity', null=False, default=0)
    
    def __str__(self):
        return str(self.Company) + " " + str(self.Series) + " " + str(self.Model)

    def json(self):
        json_data = {
            'id': self.id,
            'db_model': 'Product',
            'company': self.Company,
            'series': self.Series,
            'model': self.Model,
            'price': self.Price,
            'quantity': self.Quantity
        }
        return json_data