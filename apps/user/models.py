from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from facmasys.models import Subjects

# Make user email unique to avoid conflict logging in with email.
User._meta.get_field('email')._unique = True

# Make user fields required upon register or update.
User._meta.get_field('email').blank = False
User._meta.get_field('first_name').blank = False
User._meta.get_field('last_name').blank = False

# Create your models here.
class Profile(models.Model):
    ROLES = (
        ('faculty', 'Faculty'),
        ('depthead', 'Department Head'),
        ('researchcoor', 'Research Coordinator'),
        ('extensioncoor', 'Extension Coordinator')
    )
    SPECIALIZATION_TRACK = (
        ('Web and Mobile Development', 'Web and Mobile Development'),
        ('Service Management Program', 'Service Management Program'),
        ('Business Analytics', 'Business Analytics'),
        ('None', 'None'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='profile_icon.png', upload_to='Profile_Images')
    age = models.IntegerField(null=True,blank=True)
    user_role = models.CharField(max_length=30, choices=ROLES, default='faculty')
    
    address =  models.CharField(max_length=200, null=True, blank=True)
    city_of_residence = models.CharField(max_length=100, null=True,blank=True)
    phone = models.CharField(max_length=13, null=True,blank=True)
    spec_track = models.CharField(max_length=50, choices=SPECIALIZATION_TRACK, default='None', null=True)
    handled_subjects =  models.ManyToManyField(Subjects)
    
    def __str__(self):
        return self.user.username    
    