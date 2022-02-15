from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    CreditScore = models.IntegerField(verbose_name='Credit Score', blank=False, null=False, default=0)
    CreditLimit = models.IntegerField(verbose_name='Credit Limit', blank=True, null=True)
    Address = models.CharField(verbose_name='Address', max_length=255, null=False)

    def __str__(self):
        return self.first_name + " " + self.last_name
