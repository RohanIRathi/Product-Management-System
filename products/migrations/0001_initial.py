# Generated by Django 4.0.2 on 2022-04-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Company', models.CharField(max_length=50, verbose_name='Company')),
                ('Series', models.CharField(max_length=50, verbose_name='Series')),
                ('Model', models.CharField(max_length=50, verbose_name='Model')),
                ('Price', models.DecimalField(decimal_places=2, default=0.0, max_digits=8, verbose_name='Price of the Model')),
                ('Quantity', models.SmallIntegerField(default=0, verbose_name='Available Quantity')),
            ],
        ),
    ]
