# Generated by Django 4.1.1 on 2022-12-28 04:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('faculty_member', '0002_research_faculty_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='extensionservice',
            name='faculty_id',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
