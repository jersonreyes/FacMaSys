# Generated by Django 4.1.1 on 2022-10-15 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0010_alter_shipmentarchive_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shipmentarchive',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
