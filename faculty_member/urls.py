from django.urls import path
from . import views

"""
WAG KALIMUTANG LAGYAN SI URLS.PY NG PATH DOON SA MAIN PROJECT!!!!
"""



urlpatterns = [
    # path('subjects/details/<str:id>', views.details, name='details'),

    path('', views.faculty_member_main), # subject is the default one.
    path('subject_taught/', views.faculty_subjects_taught),
    path('subject_taught/add_subject', views.add_taught_subjects),
    
    path('researches/', views.faculty_researches),
    path('researches/add_research', views.add_researches),
    # path('researches/add_presented', views.faculty_researches),
    # path('researches/add_published', views.faculty_researches),
    
    # path('researches/update', views.faculty_researches),
    # path('researches/update_presented', views.faculty_researches),
    # path('researches/update_published', views.faculty_researches),

    
    # path('researches/delete', views.faculty_researches),

    path('extension_services/', views.faculty_extension_services),
    path('extension_services/add_service', views.add_extension_services),

    path('view_announcements/', views.faculty_announcements),
    # path('extensions/', views.extensions),
    # path('announcements/', views.announcements),
    

    
    # path('show/', views.show),
    # path('edit/<int:id>', views.edit_subject),
    # path('update/<int:id>', views.update_subject),
    # path('delete/<int:id>', views.delete_subject),
    # path('subjects/update/<int:id>', views.update),
    # path('subjects/delete/<int:id>', views.delete),
    
    
    # path('', views.register, name='main'),
    # path(''),
]