from django.shortcuts import render, redirect
from django.template import loader
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User


from django.apps import apps
Subjects_Taught = apps.get_model('faculty_member', 'Subjects_Taught')
Announcements = apps.get_model('feed', 'Announcements')


# Create your views here.

def index(request):
    all_faculty_teach = Subjects_Taught.objects.all()
    context = {
        'all_faculty_teach': all_faculty_teach
    }
    
    
    # return render(request, "department_head/index.html", context)
    return render(request, "department_head/index.html", context)
    
def show_dept_summary(request):
    return render(request, "department_head/summary.html", None)



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
