# Generated by Django 4.1.1 on 2022-09-19 01:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0019_supplier_alter_order_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplier',
            name='contact_num',
            field=models.CharField(max_length=11, null=True),
        ),
    ]
