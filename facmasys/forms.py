from django import forms
from django.apps import apps
from django.forms import ModelForm

from .models import *

Feeds = apps.get_model('feed', 'Feeds')

class FeedsForm(forms.ModelForm):
    class Meta:
        model = Feeds
        # fields = "__all__"
        exclude = ('user_id',  )

class SubjectTaughtForm(forms.ModelForm):
    class Meta:
        model = Subjects_Taught
        fields = ['handled_subjects']
        widget = {
            # 'faculty_id': forms.ChoiceField(default=request.user.id),
            'handled_subjects': forms.MultipleChoiceField(),
        }

class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subjects
        fields = "__all__"
        widget = {
            'semester': forms.ChoiceField(),
            'year': forms.ChoiceField(),
            'specialization': forms.ChoiceField(),
            'pre_requisite': forms.CheckboxSelectMultiple(),
            'course_type': forms.ChoiceField(),
        }

class ExtensionServiceForm(forms.ModelForm):
    class Meta:
        model = ExtensionService
        # fields = "__all__"
        exclude = ('faculty_id', 'ext_offeredprograms_id', 'ext_collaborator_id', )
        widget = {
            'email': forms.EmailInput(),
        }

class Research_PresentedForm(forms.ModelForm):
    class Meta:
        model = Research_Presented
        exclude = ('faculty_id',  )
        # fields = "__all__"
        widget = {
            'event_start_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'event_end_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'date_presented': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

class Research_PublishedForm(forms.ModelForm):
    class Meta:
        model = Research_Published
        exclude = ('faculty_id',  )
        # fields = "__all__"
        
class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        exclude = ('faculty_id', )
        # fields = "__all__"
        # fields = ["research_title", "research_progress", "research_area", "degree_level", "researcher_school", "presented_id", "published_id"]
        widget = {
            'research_progress': forms.ChoiceField(),
            'research_area': forms.ChoiceField(),
            'degree_level': forms.ChoiceField(),
            'document':  forms.FileField(label='Select a file', help_text='max. 42 megabytes')
        }
