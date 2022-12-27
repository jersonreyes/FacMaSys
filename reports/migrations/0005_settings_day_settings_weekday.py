# Generated by Django 4.1.1 on 2022-11-30 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0004_settings_notifications'),
    ]

    operations = [
        migrations.AddField(
            model_name='settings',
            name='day',
            field=models.PositiveIntegerField(default=1, null=True),
        ),
        migrations.AddField(
            model_name='settings',
            name='weekday',
            field=models.CharField(blank=True, choices=[('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday'), ('7', 'Sunday')], max_length=20, null=True),
        ),
    ]
