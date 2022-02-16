from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CreditScore = models.IntegerField(verbose_name='Credit Score', blank=False, null=False, default=0)
    CreditLimit = models.IntegerField(verbose_name='Credit Limit', blank=True, null=True)
    Address = models.CharField(verbose_name='Address', max_length=255, null=False)
    Contact = models.BigIntegerField(verbose_name='Mobile no.', null=False, blank=False, default=1234567890)
    Distributor = models.ForeignKey('self', null=True, verbose_name='Distributor', on_delete=models.RESTRICT)

    def __str__(self):
        return self.first_name + " " + self.last_name
