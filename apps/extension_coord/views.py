from django.shortcuts import render, redirect
from django.template import loader
from .models import *
from .forms import *
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
# def index(request):
#     extensions = ExtensionService.objects.all()
#     context = {
#         'extensions': extensions,
#     }
#     return render(request, "extension_coord/index.html", context)
    
# def show_ext_summary(request):
#     context = {
#         '': '',
#     }
#     return render(request, "announcements/summary.html", context)

# def show_ext_announcements(request):
#     announcements = Announcements.objects.all().filter(user_id=request.user)
#     context = {
#         'announcements': announcements,
#     }
#     return render(request, "announcements/announcements.html", context)


# def update_ext_announcements(request, id):
#     research = Announcements.objects.get(id=id)  
#     form = AnnouncementsForm(request.POST, instance=research)  
#     if form.is_valid():  
#         form.save()  
#         return redirect("../")  
    
#     context = {
#         'research': research,
#         'form': form,
#     }
#     return render(request, 'announcements/update_announcements.html', context)

# def delete_ext_announcements(request, id):
#     announcements = Announcements.objects.get(id=id)
#     announcements.delete()
#     return redirect("../")
