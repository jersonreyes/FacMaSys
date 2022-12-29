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
    return render(request, "extension_services/extension_services.html", {'all_extension_services': all_extension_services})

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
    return render(request, '/crud/add_extension_services.html', context) 

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
    return render(request, '/crud/update_extension_service.html', context)  

def delete_extension_services(request, id):
    ext = ExtensionService.objects.get(id=id)  
    ext.delete()  
    return redirect("../")

def faculty_member_main(request):
    # current_user = 
    return render(request, "faculty_member.html", None)

""" VIEW FUNCTIONS """
# Subject Taught 
def faculty_subjects_taught(request):
    try:
        my_subject =  Subjects_Taught.objects.get(faculty_id=request.user)
        # subject =  Subjects_Taught.filter.get(faculty_id=request.user)
    except Subjects_Taught.DoesNotExist:
        Subjects_Taught.objects.create(faculty_id=request.user)
        # subject =  Subjects_Taught.filter.get(faculty_id=request.user)
    
    context = {
        'all_subjects': my_subject.handled_subjects.all()
    }
    return render(request, "subjects/subject_taught.html", context)
    
def add_taught_subjects(request):
    
    all_subjects = Subjects_Taught.objects.get(faculty_id=request.user)
    values = list(all_subjects.handled_subjects.values())
    # print("values: ", values)
    
    selected_list = []
    for e in values:
        selected_list.append(e['id'])
    
    print('selected_list: ', selected_list)

    if request.method == "POST":  
        form = SubjectTaughtForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()
                return redirect('/')   # refresh
            except:  
                pass  
    else:  
        form = SubjectTaughtForm()  
        
    context = {
        'form': form,
        'selected_list': selected_list
    }
    return render(request, '/crud/add_subject_taught.html', context) 

def update_taught_subjects(request, id):
    all_subjects = Subjects_Taught.objects.get(faculty_id=id)
    form = SubjectTaughtForm(request.POST, instance=all_subjects)  
    if form.is_valid():  
        form.save()  
        print("Saved!")
        return redirect("../")  
    else:
        print("Noped!")
    
    context = {
        'all_subjects': all_subjects.handled_subjects.all()
    }
    return render(request, '/crud/add_subject_taught.html', context) 


def edit_extension_services(request, id):
    print('update_extension_services')
    form = ExtensionServiceForm()
    extension = ExtensionService.objects.get(id=id)
    
    context = {
        'extension': extension,
        'form': form,
    }
    return render(request, '/crud/update_extension_service.html', context)  

# Researches
def faculty_researches(request):
    research_ongoing = Research.objects.all().filter(faculty_id=request.user)
    research_ongoing_filtered = research_ongoing.filter(research_progress__exact='Ongoing')
    
    print('testestst', research_ongoing.filter(research_progress__exact='Presented'))
    
    # Baligtad hahaha
    research_presented = Research_Presented.objects.all().filter(faculty_id=request.user)
    research_published = Research_Published.objects.all().filter(faculty_id=request.user)
    

    context = {
        'research_ongoing': research_ongoing,
        'research_ongoing_filtered': research_ongoing_filtered,
        'research_presented': research_presented,
        'research_published': research_published,
    }
    return render(request, "researches/researches.html", context)

# Create your views here.
def add_researches(request):  
    user_instance = request.user
    # print(User.objects.all())
    
    if request.method == "POST":  
        form = ResearchForm(request.POST)  
        
        if form.is_valid():  
            try:  
                new_form = form.save(commit=False)
                new_form.faculty_id = user_instance
                new_form.save()
                print("Success! done") 
                return redirect('./')   # refresh
            except:  
                pass  
    else:  
        form = ResearchForm()         

        print("Failed!") 
        
    context = {
        'form': form,
        # 'form_presented': form_presented,
        # 'form_published': form_published,
    }
    return render(request, 'crud/add_researches.html', context)  

def add_presented(request):
    user_instance = request.user
    # print(User.objects.all())
    # research_presented = Research_Presented.objects.all().filter(faculty_id=request.user)
    # research_published = Research_Published.objects.all().filter(faculty_id=request.user)
    
    all_presented = Research.objects.all().filter(faculty_id=request.user)
    all_presented2 = Research_Presented.objects.all().filter(faculty_id=request.user)
    all_presented3 = Research_Presented.objects.all().filter(faculty_id=request.user)
    
    print('add_presented: ', add_presented)
    print('add_presented2: ', all_presented2)
    # # values = list(all_presented.faculty_id.values())
    # # # print("values: ", values)
    
    # # selected_list = []
    # # for e in values:
    # #     selected_list.append(e['id'])
    # # print('all_presented values: ', val)
    # print(add_presented.values)
    
    if request.method == "POST":  
        form = Research_PresentedForm(request.POST)  
        if form.is_valid():  
            try:  
                new_form = form.save(commit=False)
                new_form.faculty_id = user_instance
                new_form.save()
                print("Success!") 
                return redirect('./')   # refresh
            except:  
                pass  
    else:  
        form = Research_PresentedForm()         
        print("Failed!") 
        
    context = {
        'form': form,
        'all_presented': all_presented,
        'all_presented2': all_presented2,
    }
    return render(request, 'crud/add_presented.html', context) 
 
def add_published(request):
    user_instance = request.user
    # print(User.objects.all())
    
    all_published = Research_Published.objects.all()
    # print("values: ", values)
    
    # selected_list = []
    # for e in values:
    #     selected_list.append(e['id'])
    # print('published values: ', val)
    
    
    if request.method == "POST":  
        form = Research_PublishedForm(request.POST)  
        if form.is_valid():  
            try:  
                new_form = form.save(commit=False)
                new_form.faculty_id = user_instance
                new_form.save()
                print("Success!") 
                return redirect('./')   # refresh
            except:  
                pass  
    else:  
        form = Research_PublishedForm()
        print("Failed!") 
        
    context = {
        'form': form,
        'all_published': all_published,
    }
    return render(request, 'crud/add_published.html', context)  

# def show_updateform_researches(request, id):
#     form = ResearchForm()  
#     all_researches = Research.objects.all() 
#     research = Research.objects.get(id=id)  
    
#     context = {
#         'research': research,
#         'form': form,
#     }
#     return render(request, 'subjects/edit.html', context)  


def edit_researches(request, id):
    research = Research.objects.get(id=id)
    return render(request, 'crud/update_research_details.html', context)  
    
def update_researches(request, id):
    form = ResearchForm()  
    research = Research.objects.get(id=id)  
    form = ResearchForm(request.POST, instance=research)  
    if form.is_valid():  
        form.save()  
        return redirect("../")  
    
    context = {
        'research': research,
        'form': form,
    }
    return render(request, 'crud/update_research_details.html', context)  

""" DELETE FUNCTIONS """
def delete_researches(request, id):  
    subject = Research.objects.get(id=id)  
    subject.delete()  
    return redirect("../")

def delete_extension_services(request, id):
    ext = ExtensionService.objects.get(id=id)  
    ext.delete()  
    return redirect("../")