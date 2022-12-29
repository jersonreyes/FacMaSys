from django.forms import ModelForm
from django import forms
from .models import *

from django.apps import apps
Announcements = apps.get_model('feed', 'Announcements')

class AnnouncementsForm(forms.ModelForm):
    class Meta:
        model = Announcements
        # fields = "__all__"
        exclude = ('user_id',  )