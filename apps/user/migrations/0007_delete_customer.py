# Generated by Django 4.1.1 on 2022-12-28 15:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_profile_age_profile_city_of_residence_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Customer',
        ),
    ]
