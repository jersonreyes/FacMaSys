# Generated by Django 4.1.1 on 2022-11-07 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_icon.png', upload_to='Profile_Images'),
        ),
    ]