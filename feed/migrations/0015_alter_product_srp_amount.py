# Generated by Django 4.1.1 on 2022-09-15 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0014_alter_product_cars_alter_product_low_qty_limit_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='srp_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
    ]