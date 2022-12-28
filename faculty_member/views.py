from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from .models import *
from .forms import *
from django.contrib import messages
import csv

# with open('UpdatedSubjectLitsts.csv', mode ='r') as file:
#     csvFile = csv.reader(file)
#     # reading the CSV file

#     # displaying the contents of the CSV file
#     for lines in csvFile:
#         subj = Subjects.objects.create(course_code=lines[0], course_title=lines[1], course_credits=lines[2], semester=lines[3], year=lines[4], course_lec_units=lines[5], course_lab_units=lines[6], course_hours_per_week=lines[7], specialization="None", pre_requisite=None, course_type=lines[8])
        
#         print(f"course_code='{lines[0]}', course_title='{lines[1]}', course_credits={lines[2]}, semester='{lines[3]}', year='{lines[4]}', course_lec_units={lines[5]}, course_lab_units={lines[6]}, course_hours_per_week={lines[7]}, specialization='None', course_type={lines[8]},", end="\n\n")


# Delete everything
# Subjects.objects.all().delete()


# Create your views here.
def display_taught_subjects(request):  
    all_subjects = Subjects.objects.all()  
    return render(request, "subjects/show.html", {'all_subjects': all_subjects})  



# Home - Faculty Member
def faculty_member_main(request):
    # current_user = 
    return render(request, "faculty_member.html", None)


""" VIEW FUNCTIONS """
# Subject Taught 
def faculty_subjects_taught(request):
    print("Logged User: ", request.user.id)
    try:
        subject =  Subjects_Taught.objects.get(faculty_id=request.user)
        # subject =  Subjects_Taught.filter.get(faculty_id=request.user)
    except Subjects_Taught.DoesNotExist:
        Subjects_Taught.objects.create(faculty_id=request.user)
        # subject =  Subjects_Taught.filter.get(faculty_id=request.user)
    
    # all_subjects = 
    
    context = {
        'all_subjects': subject.handled_subjects.all()
    }
    print('context: ', subject) 
    return render(request, "faculty_member/subject_taught.html", context)
    
# Researches
def faculty_researches(request):
    all_researches = Research.objects.all() 
    return render(request, "faculty_member/researches.html", {'all_researches': all_researches})

# Extension Services
def faculty_extension_services(request):
    all_extension_services = ExtensionService.objects.all()
    return render(request, "faculty_member/extension_services.html", {'all_extension_services': all_extension_services})

# View Announcements
def faculty_announcements(request):
    announcements = (
        ("1", "BulSUFlex GCTalks Webinar", "August 24, 2020, at 8:24 PM", "All Concerned", "Department Head", "The BulSU webinar series for students will resume on Wednesday with the webinar regarding E-Learning using Google Classroom on August 26 at 2 PM. The webinar will be headed by Ms. Lilibeth Antonio MSIT, a faculty member of the College of Information and Communications Technology; and Dr. Joseline Santos, the university's Assistant Director for Student Policy Development.", "None", "None"),
        ("2", "Faculty Adviser Orientation", "September 27, 2021, at 5:54 PM", "All Concerned", "Faculty", "FACULTY ADVISER ORIENTATION Tomorrow  at 8:00 AM. Please visit the link below for the Google Meet link.", "https://bit.ly/3rdYearCICT", "None"),
    )
    
    return render(request, "faculty_member/view_announcements.html", {'announcements': announcements})


""" CREATE FUNCTIONS """
# Create your views here.
def add_researches(request):  
    if request.method == "POST":  
        form = ResearchForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()
                return redirect('/')   # refresh
            except:  
                pass  
    else:  
        form = ResearchForm()  
        
    context = {
        'form': form
    }
    return render(request, 'faculty_member/crud/add_researches.html', context)  

def add_extension_services(request):  
    if request.method == "POST":  
        form = ExtensionServiceForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()
                return redirect('/')   # refresh
            except:  
                pass  
    else:  
        form = ExtensionServiceForm()  
        
    context = {
        'form': form
    }
    return render(request, 'faculty_member/crud/add_extension_services.html', context) 


def add_taught_subjects(request):
    if request.method == "POST":  
        form = SubjectTaughtForm(request.POST, initial={"current_user": request.user})  
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
        'current_user': request.user
    }
    return render(request, 'faculty_member/crud/add_subject_taught.html', context) 
    




""" UPDATE FUNCTIONS """
def show_updateform_researches(request, id):
    all_researches = Research.objects.all() 
    research = Research.objects.get(id=id)  
    
    context = {
        'research': research,
    }
    return render(request, 'subjects/edit.html', context)  

def update_researches(request, id):
    research = Research.objects.get(id=id)  
    form = ResearchForm(request.POST, instance=research)  
    if form.is_valid():  
        form.save()  
        return redirect("subjects/")  
    
    context = {
        'research': research,
    }
    return render(request, 'subjects/edit.html', context)  

""" DELETE FUNCTIONS """
def delete_researches(request, id):  
    subject = Subjects.objects.get(id=id)  
    subject.delete()  
    return redirect("../show")

# <th>ID</th>
# <th>Subject</th>
# <th>Date of Announcement</th>
# <th>Posted To</th>
# <th>Posted From</th>
# <th>Message</th>
# <th>Links</th>
# <th>Documents</th>