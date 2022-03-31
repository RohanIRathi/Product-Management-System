from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	PendingAmount = models.DecimalField(verbose_name="Payment Amount Pending", max_digits=10, decimal_places=2, null=False, default=0.00)
	CreditScore = models.IntegerField(verbose_name='Credit Score', blank=False, null=False, default=0)
	CreditLimit = models.IntegerField(verbose_name='Credit Limit', blank=True, null=True)
	Address = models.CharField(verbose_name='Address', max_length=255, null=False)
	Contact = models.BigIntegerField(verbose_name='Mobile no.', null=False, blank=False, default=1234567890)
	Distributor = models.ForeignKey('self', verbose_name='Distributor', null=True, on_delete=models.RESTRICT)

	def __str__(self):
		return self.first_name + " " + self.last_name

	def json(self):
		if self.Distributor:
			self_distributor = self.Distributor.json()
		else:
			self_distributor = self.Distributor
		json_data = {
			'id': self.id,
			'model': 'User',
			'username': self.username,
			'first_name': self.first_name,
			'last_name': self.last_name,
			'is_superuser': self.is_superuser,
			'is_staff': self.is_staff,
			'is_active': self.is_active,
			'credit_score': self.CreditScore,
			'credit_limit': self.CreditLimit,
			'contact': self.Contact,
			'address': self.Address,
			'distributor': self_distributor
		}
		return json_data
