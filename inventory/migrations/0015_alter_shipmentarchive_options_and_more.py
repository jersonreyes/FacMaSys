# Generated by Django 4.1.1 on 2022-11-27 07:37

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0014_alter_shipment_options_shipment_gross_amount_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='shipmentarchive',
            options={'ordering': ['-date']},
        ),
        migrations.AddField(
            model_name='shipmentarchive',
            name='gross_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='shipmentarchive',
            name='base_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
        migrations.AlterField(
            model_name='shipmentarchive',
            name='fees',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, null=True, validators=[django.core.validators.MinValueValidator(Decimal('0.00'))]),
        ),
    ]
