# Generated by Django 4.0.2 on 2022-02-15 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0001_initial'),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Discount', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='Discount')),
                ('Quantity', models.SmallIntegerField(verbose_name='Quantity')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='Products',
            field=models.ManyToManyField(related_name='products', through='orders.OrderProduct', to='products.Product'),
        ),
        migrations.AlterField(
            model_name='order',
            name='DistributorId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='distributor', to=settings.AUTH_USER_MODEL, verbose_name='Distributor'),
        ),
        migrations.AlterField(
            model_name='order',
            name='RetailerId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='retailer', to=settings.AUTH_USER_MODEL, verbose_name='Retailer'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='Order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_products', to='orders.order'),
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='Product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, related_name='order_products', to='products.product'),
        ),
    ]
