# Generated by Django 4.0.2 on 2022-04-18 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('products', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('TotalQuantity', models.SmallIntegerField(default=0, verbose_name='Total Quantity')),
                ('TotalAmount', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total Amount')),
                ('CreationDate', models.DateTimeField(auto_now_add=True, verbose_name='Order Date')),
                ('PaymentDate', models.DateTimeField(blank=True, null=True, verbose_name='Order Payment Date')),
                ('DistributorId', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='distributor', to=settings.AUTH_USER_MODEL, verbose_name='Distributor')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Discount')),
                ('Quantity', models.SmallIntegerField(verbose_name='Quantity')),
                ('Order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_products', to='orders.order')),
                ('Product', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_products', to='products.product')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Products',
            field=models.ManyToManyField(related_name='products', through='orders.OrderProduct', to='products.Product'),
        ),
        migrations.AddField(
            model_name='order',
            name='RetailerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='retailer', to=settings.AUTH_USER_MODEL, verbose_name='Retailer'),
        ),
    ]
