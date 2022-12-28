from django.forms import ModelForm
from django import forms
from .models import *


class UsersForm(forms.ModelForm):
    class Meta:
        models = Users
        widget = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput(),
        }

class SubjectTaughtForm(forms.ModelForm):
    class Meta:
        model = Subjects_Taught
        fields = "__all__"
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
        widget = {
            'email': forms.EmailInput(),
        }

class Research_Presented(forms.ModelForm):
    class Meta:
        models = Research_Presented
        fields = "__all__"

class Research_Published(forms.ModelForm):
    class Meta:
        model = Research_Published
        fields = "__all__"
        
class ResearchForm(forms.ModelForm):
    class Meta:
        model = Research
        fields = "__all__"
        widget = {
            'research_progress': forms.ChoiceField(),
            'research_area': forms.ChoiceField(),
            'degree_level': forms.ChoiceField(),
        }