# Generated by Django 4.1.1 on 2022-09-11 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_alter_order_options_alter_product_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name_plural': 'Product'},
        ),
        migrations.AlterField(
            model_name='order',
            name='staff',
            field=models.CharField(max_length=200, null=True),
        ),
    ]