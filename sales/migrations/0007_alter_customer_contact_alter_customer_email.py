# Generated by Django 4.1.1 on 2022-10-04 22:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0006_rename_car_customer_car_make_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='contact',
            field=models.CharField(max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(max_length=254, null=True, unique=True),
        ),
    ]
