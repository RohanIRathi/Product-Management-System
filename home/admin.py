from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
	readonly_fields = ('password',)
	fieldsets = (
		('Important', {
			"fields": (
				'username', 'password'
			),
		}),
		('Personal info', {
			'fields': ('first_name', 'last_name', 'email')
		}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Other Info', {
			'fields': ('PendingAmount', 'CreditScore', 'CreditLimit', 'Address', 'Contact', 'Distributor')
		}),
	)
	

	def lookup_allowed(self, lookup, value):
        # Don't allow lookups involving passwords.
		return not lookup.startswith('password') and super().lookup_allowed(lookup, value)

# Register your models here.
admin.site.register(User, UserAdmin)