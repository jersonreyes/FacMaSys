# Generated by Django 4.1.1 on 2022-11-29 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_alter_activitylog_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activitylog',
            options={'ordering': ('-datetime',)},
        ),
    ]