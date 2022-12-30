from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import RequestContext, loader
from django.template.loader import render_to_string
from facmasys.utils import add_activity

from .forms import *
from .models import *

# from facmasys.forms import ExtensionServiceForm



# Create your views here.
def index(request):
    return render(request, 'home/index.html', {'state':'home'})

from django.apps import apps

Feeds_DepartmentHead = apps.get_model('feed', 'Feeds_DepartmentHead')
Feeds_ResearchCoord = apps.get_model('feed', 'Feeds_ResearchCoord')
Feeds_ExtensionCoord = apps.get_model('feed', 'Feeds_ExtensionCoord')

Feeds = apps.get_model('feed', 'Feeds')
Profile = apps.get_model('user', 'Profile')

# Create your views here.
""" Department Head """
@login_required
def show_dept_summary(request):
    return render(request, "subjects/summary.html", None)


@login_required
def show_ext_announcements(request):
    announcements = Feeds.objects.all().filter(user_id=request.user)
    context = {
        'announcements': announcements,
        'state':'extension_services',
    }
    return render(request, "announcements/announcements.html", context)


@login_required
def update_ext_announcements(request, id):
    if not request.user.profile.user_role == 'faculty' or request.user.is_superuser:
        research = Feeds.objects.get(id=id)  
        form = Feeds(request.POST, instance=research)  
        if form.is_valid():  
            form.save()
            add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='EXT ANNOUNCEMENT',activity_message=f"User {request.user.username} updated an ext announcement.")
            return redirect("/feed")  
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'research': research,
            'form': form,
            'state':'extension_services',
        }
        return render(request, 'announcements/update_announcements.html', context)
    return redirect('index')

@login_required
def delete_ext_announcements(request, id):
    if not request.user.profile.user_role == 'faculty' or request.user.is_superuser:
        announcements = Feeds.objects.get(id=id)
        announcements.delete()
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='EXT ANNOUNCEMENT',activity_message=f"User {request.user.username} deleted an ext announcement.")
        return redirect("/feed")
    return redirect('index')

@login_required
def add_announcements(request):

    profile = Profile.objects.filter(user=request.user).values().first()
    
    user_instance = request.user
    if request.method == "POST":  
        form = FeedsForm(request.POST, request.FILES)  
        # Extension Coordinator
        if request.user.profile.user_role == 'extensioncoor':
            form2 = Feeds_ExtensionCoordForm(request.POST)

        # Department Head
        elif request.user.profile.user_role == 'depthead':
            form2 = Feeds_DepartmentHeadForm(request.POST)
            
        # Research Coordinator
        elif request.user.profile.user_role == 'researchcoor':
            form2 = Feeds_ResearchCoordForm(request.POST)
        
        # Faculty
        else:
            form = Feeds()
            form2 = FeedsForm() # submit invalid form
        
        print('Starting...')
        
        if form.is_valid() and form2.is_valid():  
            try:  
                new_form = form.save(commit=False)
                new_form.user_id = user_instance
                print('ID: ', form.cleaned_data)
                new_form.save()
                
                # form2.save()
                recent_add = Feeds.objects.last()
                print("recent_add: ", recent_add)
                
            
                new_form2 = form2.save(commit=False)
                new_form2.reference_id = recent_add
                new_form2.save()

                print('new_form: ', new_form)
                print('new_form2: ', new_form2)
                print("end")
                add_activity(logged_user=request.user,activity_type='ADD',activity_location='ANNOUNCEMENT',activity_message=f"User {request.user.username} added an announcement.")
                return redirect('feed')   # refresh
            except:  
                pass  
        else:
            print("Invalid Form!")
    else:  
        form = FeedsForm()         
        # Extension Coordinator
        if request.user.profile.user_role == 'extensioncoor':
            form2 = Feeds_ExtensionCoordForm()
        elif request.user.profile.user_role == 'depthead':
            form2 = Feeds_DepartmentHeadForm()
        elif request.user.profile.user_role == 'researchcoor':
            form2 = Feeds_ResearchCoordForm()
        else:
            form2 = FeedsForm() # set invalid form    
            
        print("Failed sadge!") 
        
    context = {
        'form': form,
        'form2': form2,
        'state':'announcements',
        'user_type': profile['user_role'],
    }
    
    
    # if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    #     return redirect("../") 
    return render(request, 'announcements/add_announcements.html', context)

    
    
""" ANNOUNCEMENTS """
@login_required
def show_announcements(request):
    announcements = Feeds.objects.all().filter(user_id=request.user)
    profile = Profile.objects.filter(user=request.user).values().first()

    
    context = {
        'announcements': announcements,
        'state':'announcements',
        'user_type': profile['user_role'],
    }
    
    # Extension Coordinator
    if request.user.profile.user_role == 'extensioncoor':
        ext_coord = Feeds_ExtensionCoord.objects.all()
        context['announcements2'] = ext_coord

    # Department Head
    elif request.user.profile.user_role == 'depthead':
        dpt_head = Feeds_DepartmentHead.objects.all()
        context['announcements2'] = dpt_head
        
    # Research Coordinator
    elif request.user.profile.user_role == 'researchcoor':
        research_coord = Feeds_ResearchCoord.objects.all()
        context['announcements2'] = research_coord
        
    else:
        # Faculty Announcement Lists
        context['vext'] = Feeds_ExtensionCoord.objects.all()
        context['dpt'] = Feeds_DepartmentHead.objects.all()
        context['rsh'] = Feeds_ResearchCoord.objects.all()
        

    
    return render(request, "announcements/announcements.html", context)

@login_required
def update_announcements(request, id):
    # if not request.user.profile.user_role == 'faculty' or request.user.is_superuser:
    research = Feeds.objects.get(id=id)  
    profile = Profile.objects.filter(user=request.user).values().first()
    form = FeedsForm(request.POST, request.FILES, instance=research)  
    
        # Extension Coordinator
    if request.user.profile.user_role == 'extensioncoor':
        research2 = Feeds_ExtensionCoord.objects.get(reference_id=research)  
        form2 = Feeds_ExtensionCoordForm(request.POST, instance=research2)
        print('extensioncoor')

    # Department Head
    elif request.user.profile.user_role == 'depthead':
        research2 = Feeds_DepartmentHead.objects.get(reference_id=research)  
        form2 = Feeds_DepartmentHeadForm(request.POST, instance=research2)
        print('depthead')
        
    # Research Coordinator
    elif request.user.profile.user_role == 'researchcoor':
        research2 = Feeds_ResearchCoord.objects.get(reference_id=research)  
        form2 = Feeds_ResearchCoordForm(request.POST, instance=research2)
        print('researchcoor')

    
    if form.is_valid() and form2.is_valid():  
        print("True")
        
        form.save()
        add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='ANNOUNCEMENT',activity_message=f"User {request.user.username} updated an announcement.")
        return redirect("feed")
    
    # Ayaw pumuta sa update dahil dito
    # if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
    #     return redirect("../") 
    
    print("False")
    context = {
        'research': research,
        'research2': research2,
        
        'form': form,
        'form2': form2,

        'state': 'announcements',
        'user_type': profile['user_role'],
    }
    return render(request, 'announcements/update_announcements.html', context)
    # return redirect('index')

@login_required
def delete_announcements(request, id):
    if not request.user.profile.user_role == 'faculty' or request.user.is_superuser:
        announcements = Feeds.objects.get(id=id)
        announcements.delete()
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='ANNOUNCEMENT',activity_message=f"User {request.user.username} deleted an announcement.")
        return redirect("/feed/")
    return redirect('index')

from django.shortcuts import get_object_or_404, render


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
    
def permission_denied(request, exception):
    return render(request, '403.html', status=403)

def bad_request(request, exception):
    return render(request, '400.html', status=400)

def server_error(request, *args, **argv):
    return render(request, '500.html', status=500)

@login_required
def faculty_extension_services(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser:
        all_extension_services = ExtensionService.objects.all().filter(faculty_id=request.user)
        return render(request, "extension_services/extension_services.html", {'all_extension_services': all_extension_services})
    return redirect('index')

@login_required
def add_extension_services(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser: 
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
                    add_activity(logged_user=request.user,activity_type='ADD',activity_location='EXTENSION SERVICE',activity_message=f"User {request.user.username} added an extension service.")
                    print("Success!") 
                    return redirect('extension_services-index')   # refresh
                except:  
                    pass  
            else:
                print("not valid") 
        else:  
            form = ExtensionServiceForm()         
            print("Failed!") 
            
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'form': form,
            'state':'extension_services',
        }
        return render(request, 'extension_services/add_extension_services.html', context)
    return redirect('index')

@login_required
def edit_extension_services(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser:
        print('update_extension_services')
        form = ExtensionServiceForm()
        extension = ExtensionService.objects.get(id=id)
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'extension': extension,
            'form': form,
            'state':'extension_services',
        }
        return render(request, 'extension_services/update_extension_service.html', context)
    return redirect('index')

@login_required
def update_extension_services(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser:
        extension = ExtensionService.objects.get(id=id)  
        form = ExtensionServiceForm(request.POST, instance=extension)  
        if form.is_valid():  
            form.save()  
            add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='EXTENSION SERVICE',activity_message=f"User {request.user.username} updated an extension service.")
            return redirect("/extension_services")  
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'extension': extension,
            'form': form,
            'state':'extension_services',
        }
        return render(request, 'extension_services/update_extension_service.html', context)
    return redirect('index')

@login_required
def delete_extension_services(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser:
        ext = ExtensionService.objects.get(id=id)  
        ext.delete()  
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='EXTENSION SERVICE',activity_message=f"User {request.user.username} deleted an extension service.")
        return redirect("/extension_services")
    return redirect('index')

def faculty_member_main(request):
    # current_user = 
    return render(request, "faculty_member.html", None)

""" VIEW FUNCTIONS """
# Subject Taught 
@login_required
def faculty_subjects_taught(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        try:
            my_subject =  Subjects_Taught.objects.get(faculty_id=request.user)
            # subject =  Subjects_Taught.filter.get(faculty_id=request.user)
        except Subjects_Taught.DoesNotExist:
            Subjects_Taught.objects.create(faculty_id=request.user)
            # subject =  Subjects_Taught.filter.get(faculty_id=request.user)
        
        context = {
            'all_subjects': my_subject.handled_subjects.all(),
            'state':'subjects_taught',
        }
        return render(request, "subjects/subject_taught.html", context)
    return redirect('index')
    
@login_required
def add_taught_subjects(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
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
                    add_activity(logged_user=request.user,activity_type='ADD',activity_location='SUBJECT TAUGHT',activity_message=f"User {request.user.username} added subject taught.")
                    return redirect('/subjects/')   # refresh
                except:  
                    pass  
        else:  
            form = SubjectTaughtForm()  
            
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
            
        context = {
            'form': form,
            'selected_list': selected_list,
            'state':'subjects_taught',
        }
        return render(request, 'subjects/add_subject_taught.html', context)
    return redirect('index')

@login_required
def update_taught_subjects(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        all_subjects = Subjects_Taught.objects.get(faculty_id=id)
        form = SubjectTaughtForm(request.POST, instance=all_subjects)  
        if form.is_valid():  
            form.save()  
            add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='SUBJECT TAUGHT',activity_message=f"User {request.user.username} updated subject taught.")
            print("Saved!")
            return redirect('/subjects/')
        else:
            print("Noped!")
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'all_subjects': all_subjects.handled_subjects.all(),
            'state':'subjects_taught',
        }
        return render(request, 'subjects/add_subject_taught.html', context) 
    return redirect('index')

@login_required
def edit_extension_services(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser:
        print('update_extension_services')
        
        currently_logged = ExtensionService.objects.filter(id=id)  
        current_edit = currently_logged.values().first()['extension_head_id']
        # print('current_edit: ', current_edit)
        
        form = ExtensionServiceForm()
        extension = ExtensionService.objects.get(id=id)
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'extension': extension,
            'form': form,
            'state':'extension_services',
            'current_edit': current_edit,
        }
        return render(request, 'extension_services/update_extension_service.html', context)
    return redirect('index') 

# Researches
@login_required
def faculty_researches(request):
    if request.user.profile.user_role != 'faculty' or request.user.is_superuser:
        research_ongoing = Research.objects.all().filter(faculty_id=request.user)
        research_ongoing_filtered = research_ongoing.filter(research_progress__exact='Ongoing')
        
        # print('testestst', research_ongoing.filter(research_progress__exact='Presented'))
        
        # Baligtad hahaha
        research_presented = Research_Presented.objects.all().filter(faculty_id=request.user)
        research_published = Research_Published.objects.all().filter(faculty_id=request.user)
    

        context = {
            'research_ongoing': research_ongoing,
            'research_ongoing_filtered': research_ongoing_filtered,
            'research_presented': research_presented,
            'research_published': research_published,
            'state':'researches',
        }
        return render(request, "researches/researches.html", context)
    return redirect('index')

# Create your views here.
def add_researches(request):  
    user_instance = request.user
    # print(User.objects.all())
    
    if request.method == "POST":  
        form = ResearchForm(request.POST, request.FILES)  
        
        if form.is_valid():  
            try:  
                new_form = form.save(commit=False)
                new_form.faculty_id = user_instance
                new_form.save()
                add_activity(logged_user=request.user,activity_type='ADD',activity_location='RESEARCH',activity_message=f"User {request.user.username} added a research.")
                print("Success! done") 
                return redirect('/researches/')   # refresh
            except:  
                pass  
    else:  
        form = ResearchForm()         

        print("Failed!") 
        # print('testestst', research_ongoing.filter(research_progress__exact='Presented'))
        
        # Baligtad hahaha
        research_presented = Research_Presented.objects.all().filter(faculty_id=request.user)
        research_published = Research_Published.objects.all().filter(faculty_id=request.user)
        

        context = {
            'research_ongoing': research_ongoing,
            'research_ongoing_filtered': research_ongoing_filtered,
            'research_presented': research_presented,
            'research_published': research_published,
            'state':'researches',
        }
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        return render(request, "researches/researches.html", context)
    return redirect('index')

@login_required
def add_researches(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        user_instance = request.user
        # print(User.objects.all())
        
        if request.method == "POST":
            form = ResearchForm(request.POST, request.FILES)
            
            if form.is_valid():  
                try:  
                    new_form = form.save(commit=False)
                    new_form.faculty_id = user_instance
                    new_form.save()
                    add_activity(logged_user=request.user,activity_type='ADD',activity_location='RESEARCH',activity_message=f"User {request.user.username} added a research.")
                    print("Success! done") 
                    return redirect('/researches/')   # refresh
                except:  
                    pass  
        else:  
            form = ResearchForm()         

            print("Failed!") 
            
        context = {
            'form': form,
            # 'form_presented': form_presented,
            # 'form_published': form_published,
            'state':'researches',
        }
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        return render(request, 'researches/add_researches.html', context)
    return redirect('index') 

@login_required
def add_presented(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
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
                    add_activity(logged_user=request.user,activity_type='ADD',activity_location='RESEARCH PRESENTED',activity_message=f"User {request.user.username} added a presented research.")
                    print("Success!") 
                    return redirect('/researches/')   # refresh
                except:  
                    pass  
        else:  
            form = Research_PresentedForm()         
            print("Failed!") 
            
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 

        context = {
            'form': form,
            'all_presented': all_presented,
            'all_presented2': all_presented2,
            'state':'researches',
        }
        return render(request, 'researches/add_presented.html', context) 
    return redirect('index')
 
@login_required
def add_published(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        user_instance = request.user
        # print(User.objects.all())
        
        all_published = Research_Published.objects.all()
        # print("values: ", values)
        
        # selected_list = []
        # for e in values:
        #     selected_list.append(e['id'])
        # print('published values: ', val)
        
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        if request.method == "POST":  
            form = Research_PublishedForm(request.POST)  
            if form.is_valid():  
                try:  
                    new_form = form.save(commit=False)
                    new_form.faculty_id = user_instance
                    new_form.save()
                    add_activity(logged_user=request.user,activity_type='ADD',activity_location='RESEARCH PUBLISHED',activity_message=f"User {request.user.username} added a published research.")
                    print("Success!") 
                    return redirect('/researches/')  # refresh
                except:  
                    pass  
        else:  
            form = Research_PublishedForm()
            print("Failed!") 
            
        context = {
            'form': form,
            'all_published': all_published,
            'state':'researches',
        }
        return render(request, 'researches/add_published.html', context)
    return redirect('index')

# def show_updateform_researches(request, id):
#     form = ResearchForm()  
#     all_researches = Research.objects.all() 
#     research = Research.objects.get(id=id)  
    
#     context = {
#         'research': research,
#         'form': form,
#     }
#     return render(request, 'subjects/edit.html', context)  

@login_required
def edit_researches(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        research = Research.objects.get(id=id)
        context = {
            
        }
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        return render(request, 'researches/update_research_details.html', context)
    return redirect('index')
    
@login_required
def update_researches(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        form = ResearchForm()  
        research = Research.objects.get(id=id)  
        form = ResearchForm(request.POST, request.FILES, instance=research)  
        if form.is_valid():  
            form.save()  
            add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='RESEARCH',activity_message=f"User {request.user.username} updated a research.")
            return redirect("/researches/")  
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../")  
        
        context = {
            'research': research,
            'form': form,
            'state':'researches',
        }
        return render(request, 'researches/update_research_details.html', context)
    return redirect('index') 

@login_required
def update_details_a(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        research = Research_Presented.objects.get(id=id)  
        research_all = Research_Presented.objects.filter(id=id)  
        form = Research_PresentedForm(request.POST, instance=research) 
        current_edit = research_all.values().first()['faculty_id_id']
        
        if form.is_valid():  
            print("Done!")
            form.save()
            add_activity(logged_user=request.user,activity_type='ADD',activity_location='RESEARCH PRESENTED',activity_message=f"User {request.user.username} updated a presented research.")
            return redirect("/researches/")  
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        print("asfdasfd!")
        context = {
            'research': research,
            'form': form,
            'state':'researches',
            'current_edit': current_edit,
        }
        return render(request, 'researches/update_details.html', context)
    return redirect('index')

@login_required
def update_details_b(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        research = Research_Published.objects.get(id=id)  
        form = Research_PublishedForm(request.POST, instance=research)  
        if form.is_valid():  
            form.save()  
            add_activity(logged_user=request.user,activity_type='ADD',activity_location='RESEARCH PUBLISHED',activity_message=f"User {request.user.username} added a published research.")
            return redirect("/researches/")  
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 

        research_all = Research_Published.objects.filter(id=id)  
        current_edit__ = research_all.values().first()['published_id_id']
        print('ccc', current_edit__)
        
        context = {
            'research': research,
            'form': form,
            'state':'researches',
            'current_edit': current_edit__,
            'is_other': True,
        }
        return render(request, 'researches/update_details.html', context)
    return redirect('index')



""" DELETE FUNCTIONS """
@login_required
def delete_details_a(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        subject = Research_Presented.objects.get(id=id)  
        subject.delete()  
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='RESEARCH PRESENTED',activity_message=f"User {request.user.username} deleted a presented research.")
        return redirect("/researches/")
    return redirect('index')

@login_required
def delete_details_b(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        subject = Research_Published.objects.get(id=id)  
        subject.delete()  
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='RESEARCH PUBLISHED',activity_message=f"User {request.user.username} added a published research.")
        return redirect("/researches/")
    return redirect('index')

@login_required
def delete_researches(request, id):  
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'researchcoor' or request.user.is_superuser:
        subject = Research_Published.objects.get(id=id)  
        subject.delete()
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='RESEARCH',activity_message=f"User {request.user.username} deleted a research.")
        return redirect("/researches/")
    return redirect('index')

@login_required
def delete_extension_services(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'extensioncoor' or request.user.is_superuser:
        ext = ExtensionService.objects.get(id=id)  
        ext.delete()  
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='EXTENSION SERVICE',activity_message=f"User {request.user.username} deleted an extension service.")
        return redirect("/extension_services/")
    return redirect('index')


""" SUBJECTS """
@login_required
def show_subject(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        all_subjects = Subjects.objects.all()
        context = {
            'all_subjects': all_subjects,
            'state':'subjects',
        }
        return render(request, "subjects/subjects.html", context)
    return redirect('index')

@login_required
def add_subject(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        if request.method == "POST":  
            form = SubjectForm(request.POST)  
            if form.is_valid():
                print("is valid")   
                try:  
                    form.save()
                    add_activity(logged_user=request.user,activity_type='ADD',activity_location='SUBJECT',activity_message=f"User {request.user.username} added a subject.")
                    print("Success!") 
                    return redirect('/subjects/')   # refresh
                except:  
                    pass  
            else:
                print("not valid") 
        else:  
            form = SubjectForm()         
            print("Failed!") 
            
        context = {
            'form': form,
            'state':'subjects',
        }
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        return render(request, 'subjects/add_subjects.html', context) 
    return redirect('index')

@login_required
def updateform_subject(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        form = SubjectForm()
        subjecttt = Subjects.objects.get(id=id)
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'subjecttt': subjecttt,
            'form': form,
            'state':'subjects',
        }
        return render(request, 'subjects/update_subjects.html', context)
    return redirect('index') 

@login_required
def update_subject(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        # all_subjects = Subjects.objects.get(id=id)
        
        # values = list(all_subjects.pre_requisite)
        # print("values: ", values)
        # selected_list = []
        # for e in values:
        #     selected_list.append(e['id'])
        
        
        subjecttt = Subjects.objects.get(id=id)  
        form = SubjectForm(request.POST, instance=subjecttt)  
        
        subject_all = Subjects.objects.all()
        current_edit = subject_all.values()
        # all_subjects = []
        # for x in current_edit:
        #     print(list[x])
        # print(all_subjects)
        
        

        subject_object_data = current_edit
        
        # print('asdfasdfsaf')
        # print("all subjects: ", current_edit)
        
        if form.is_valid():  
            form.save()  
            add_activity(logged_user=request.user,activity_type='UPDATE',activity_location='SUBJECT',activity_message=f"User {request.user.username} updated a subject.")
            return  redirect("/subjects")
        if not request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
            return redirect("../") 
        context = {
            'subjecttt': subjecttt,
            'form': form,
            'state':'subjects',
            'subject_object_data': subject_object_data,
        }
        return render(request, 'subjects/update_subjects.html', context)
    return redirect('index') 

@login_required
def delete_subject(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        ext = Subjects.objects.get(id=id)  
        ext.delete()  
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='SUBJECT',activity_message=f"User {request.user.username} deleted a subject.")
        return redirect("/subjects")
    return redirect('index')

def delete_subject_taught(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        ext = Subjects_Taught.objects.get(id=id)  
        ext.delete()  
        add_activity(logged_user=request.user,activity_type='DELETE',activity_location='SUBJECT TAUGHT',activity_message=f"User {request.user.username} deleted a subject taught.")
        return redirect("/subjects")
    return redirect('index')

""" SUBJECTS """
# import csv
# with open('UpdatedSubjectLitsts.csv', mode ='r') as file:
#     csvFile = csv.reader(file)
#     # reading the CSV file

#     # displaying the contents of the CSV file
#     for lines in csvFile:
#         subj = Subjects.objects.create(course_code=lines[0], course_title=lines[1], course_credits=lines[2], semester=lines[3], year=lines[4], course_lec_units=lines[5], course_lab_units=lines[6], course_hours_per_week=lines[7], specialization="None", pre_requisite=None, course_type=lines[8])
        
#         print(f"course_code='{lines[0]}', course_title='{lines[1]}', course_credits={lines[2]}, semester='{lines[3]}', year='{lines[4]}', course_lec_units={lines[5]}, course_lab_units={lines[6]}, course_hours_per_week={lines[7]}, specialization='None', course_type={lines[8]},", end="\n\n")


# Delete everything
# Subjects.objects.all().delete()


@login_required
def departments(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        all_department = Departments.objects.all()        

        all_faculty = Profile.objects.all().select_related('user').filter(user_role='faculty').values()
        form = DeparmentsForm()
        
        context = {
            'all_department': all_department,
            'all_faculty': all_faculty,
            'form': form,
        }
        
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        if request.method == "POST":  
            all_department = Departments.objects.all()        
            all_faculty = Profile.objects.all().select_related('user').filter(user_role='faculty').values()
            
           
            # facmasys_subjects
            # facmasys_subjects_taught
            # facmasys_subjects_taught_handled_subjects
            # print('all_subject_taught', all_subject_taught)
            
            form = DeparmentsForm(request.POST)  
            
            if form.is_valid():
                print("is valid")   
                try:  
                    form.save()
                    print("Success!") 
                    return redirect('../')   # refresh
                except:  
                    pass  
            else:
                print("not valid") 
        else:  
            form = DeparmentsForm()         
            print("Failed!")
            
        context = {
            'all_department': all_department,
            'all_faculty': all_faculty,
            'form': form,
        }
        
        return render(request, 'department/department.html', context)
    return redirect('index')


@login_required
def departments_addfaculty(request):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        all_subjects = Subjects_Taught.objects.get(faculty_id=request.user)
        
        if request.method == "POST":  
            form = SubjectTaughtForm(request.POST)  
            if form.is_valid():  
                try:  
                    form.save()
                    return redirect('/subjects/')   # refresh
                except:  
                    pass  
        else:  
            form = SubjectTaughtForm()  

            
        context = {
            'form': form,
            'state':'subjects_taught',
        }
        
        return render(request, 'department/department.html', context)
    return redirect('./')


@login_required
def departments_addsubjects(request, id):
    if request.user.profile.user_role == 'faculty' or request.user.profile.user_role == 'depthead' or request.user.is_superuser:
        print("Start!")
        
        # user_instance = request.user
        if request.method == "POST":  
            print("Start posting")
            # all_subjects = Subjects_Taught.objects.get(faculty_id=id)
            form = SubjectTaughtForm(request.POST)  
            
            
            print(form.request.POST(''))
            if form.is_valid():  
                print("Vlaid")
                new_form = form.save(commit=False)
                new_form.faculty_id_id = id
                new_form.save()
                try:  
                    return redirect('../')   # refresh
                except:  
                    pass  
        else:  
            form = SubjectTaughtForm()  
            print("Failed!")
        

        context = {
            'form': form,
            'state':'subjects_taught',
        }
        
        return render(request, "department/add_facultysubjects.html", context)
    return redirect('../')