from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.template.loader import render_to_string

from facmasys.forms import ExtensionServiceForm

from .forms import *
from .models import *
import csv


# Create your views here.
def index(request):
    return render(request, 'home/index.html', {'state':'home'})

from django.apps import apps

Announcements = apps.get_model('feed', 'Announcements')

# Create your views here.


""" Department Head """
def show_dept_summary(request):
    return render(request, "department_head/summary.html", None)

def show_ext_summary(request):
    context = {
        '': '',
    }
    return render(request, "announcements/summary.html", context)
def show_ext_announcements(request):
    announcements = Announcements.objects.all().filter(user_id=request.user)
    context = {
        'announcements': announcements,
    }
    return render(request, "announcements/announcements.html", context)
def update_ext_announcements(request, id):
    research = Announcements.objects.get(id=id)  
    form = AnnouncementsForm(request.POST, instance=research)  
    if form.is_valid():  
        form.save()  
        return redirect("../")  
    
    context = {
        'research': research,
        'form': form,
    }
    return render(request, 'announcements/update_announcements.html', context)
def delete_ext_announcements(request, id):
    announcements = Announcements.objects.get(id=id)
    announcements.delete()
    return redirect("../")




def add_announcements(request):
    user_instance = request.user
    if request.method == "POST":  
        form = AnnouncementsForm(request.POST)  
        
        if form.is_valid():  
            try:  
                new_form = form.save(commit=False)
                new_form.user_id = user_instance
                new_form.save()
                print("Success! done") 
                return redirect('./')   # refresh
            except:  
                pass  
    else:  
        form = AnnouncementsForm()         
        print("Failed sadge!") 
        
    context = {
        'form': form,
    }
    return render(request, 'announcements/add_announcements.html', context)  
    
def show_announcements(request):
    announcements = Announcements.objects.all().filter(user_id=request.user)
    context = {
        'announcements': announcements,
    }
    return render(request, "announcements/announcements.html", context)


def update_announcements(request, id):
    research = Announcements.objects.get(id=id)  
    form = AnnouncementsForm(request.POST, instance=research)  
    if form.is_valid():  
        form.save()  
        return redirect("../")  
    
    context = {
        'research': research,
        'form': form,
    }
    return render(request, 'announcements/update_announcements.html', context)

def delete_announcements(request, id):
    announcements = Announcements.objects.get(id=id)
    announcements.delete()
    return redirect("../")
from django.shortcuts import get_object_or_404, render


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
    
def permission_denied(request, exception):
    return render(request, '403.html', status=403)

def bad_request(request, exception):
    return render(request, '400.html', status=400)

def server_error(request, *args, **argv):
    return render(request, '500.html', status=500)

def faculty_extension_services(request):
    all_extension_services = ExtensionService.objects.all().filter(faculty_id=request.user)
    return render(request, "extension_services.html", {'all_extension_services': all_extension_services})

def add_extension_services(request):  
    user_instance = request.user
    
    print("Checking...") 
    if request.method == "POST":  
        print("Checking... POST") 
        form = ExtensionServiceForm(request.POST)  
        if form.is_valid():
            print("is valid")   
            try:  
                new_form = form.save(commit=False)
                new_form.faculty_id = user_instance
                new_form.save()
                print("Success!") 
                return redirect('./')   # refresh
            except:  
                pass  
        else:
            print("not valid") 
    else:  
        form = ExtensionServiceForm()         
        print("Failed!") 
        
    context = {
        'form': form
    }
    return render(request, 'faculty_member/crud/add_extension_services.html', context) 

def edit_extension_services(request, id):
    print('update_extension_services')
    form = ExtensionServiceForm()
    extension = ExtensionService.objects.get(id=id)
    
    context = {
        'extension': extension,
        'form': form,
    }
    return render(request, 'crud/update_extension_service.html', context)  

def update_extension_services(request, id):
    extension = ExtensionService.objects.get(id=id)  
    form = ExtensionServiceForm(request.POST, instance=extension)  
    if form.is_valid():  
        form.save()  
        return redirect("../")  
    
    context = {
        'extension': extension,
        'form': form,
    }
    return render(request, 'faculty_member/crud/update_extension_service.html', context)  

def delete_extension_services(request, id):
    ext = ExtensionService.objects.get(id=id)  
    ext.delete()  
    return redirect("../")



# with open('UpdatedSubjectLitsts.csv', mode ='r') as file:
#     csvFile = csv.reader(file)
#     # reading the CSV file

#     # displaying the contents of the CSV file
#     for lines in csvFile:
#         subj = Subjects.objects.create(course_code=lines[0], course_title=lines[1], course_credits=lines[2], semester=lines[3], year=lines[4], course_lec_units=lines[5], course_lab_units=lines[6], course_hours_per_week=lines[7], specialization="None", pre_requisite=None, course_type=lines[8])
        
#         print(f"course_code='{lines[0]}', course_title='{lines[1]}', course_credits={lines[2]}, semester='{lines[3]}', year='{lines[4]}', course_lec_units={lines[5]}, course_lab_units={lines[6]}, course_hours_per_week={lines[7]}, specialization='None', course_type={lines[8]},", end="\n\n")


# Delete everything
# Subjects.objects.all().delete()

def show_subject(request):
    all_subjects = Subject.objects.all()
    return render(request, "subjects/extension_services.html", {'all_subjects': all_subjects})

def add_subject(request):
    if request.method == "POST":  
        form = SubjectForm(request.POST)  
        if form.is_valid():
            print("is valid")   
            try:  
                form.save()
                print("Success!") 
                return redirect('./')   # refresh
            except:  
                pass  
        else:
            print("not valid") 
    else:  
        form = SubjectForm()         
        print("Failed!") 
        
    context = {
        'form': form
    }
    return render(request, 'subjects/add_extension_services.html', context) 


def updateform_subject(request):
    form = SubjectForm()
    subjecttt = ExtensionService.objects.get(id=id)
    
    context = {
        'subjecttt': subjecttt,
        'form': form,
    }
    return render(request, 'crud/update_subjects.html', context)  


def update_subject(request):
    subjecttt = Subject.objects.get(id=id)  
    form = SubjectForm(request.POST, instance=subjecttt)  
    if form.is_valid():  
        form.save()  
        return redirect("../")  
    
    context = {
        'subjecttt': subjecttt,
        'form': form,
    }
    return render(request, 'subjects/update_subjects.html', context)  


def delete_subject(request, id):
    ext = ExtensionService.objects.get(id=id)  
    ext.delete()  
    return redirect("../")

""" SUBJECTS """
