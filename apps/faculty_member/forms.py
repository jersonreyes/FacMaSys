from django.forms import ModelForm
from django import forms
from .models import *



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
        fields = "__all__"
        exclude = ('faculty_id', 'ext_offeredprograms_id', 'ext_collaborator_id', )
        widget = {
            'email': forms.EmailInput(),
        }

class Research_PresentedForm(forms.ModelForm):
    class Meta:
        model = Research_Presented
        exclude = ('faculty_id',  )
        fields = "__all__"
        widget = {
            'event_start_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'event_end_date': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
            'date_presented': forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
        }

class Research_PublishedForm(forms.ModelForm):
    class Meta:
        model = Research_Published
        exclude = ('faculty_id',  )
        fields = "__all__"
        
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
        }