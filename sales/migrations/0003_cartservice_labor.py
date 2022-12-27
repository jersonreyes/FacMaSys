# Generated by Django 4.1.1 on 2022-10-02 10:39

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0002_cartservice_cartproduct'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartservice',
            name='labor',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7, validators=[django.core.validators.MinValueValidator(Decimal('0.01'))]),
        ),
    ]
