from django.contrib.auth.models import User
from django.db import models


class ActivityLog(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, null=True)
    location = models.CharField(max_length=50, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.type} {self.location}'
    
    class Meta:
        ordering = ('-datetime',)
     
        
class Notifications(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True)
    read = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.message}'
    
    class Meta:
        ordering = ('-date',)
        
        
class EmailNotification(models.Model):
    FREQUENCY = (
    ("Daily", "Daily"),
    ("Weekly", "Weekly"),
    ("Monthly", "Monthly"),
    )
    
    WEEKDAYS = (
    ("1", "Monday"),
    ("2", "Tuesday"),
    ("3", "Wednesday"),
    ("4", "Thursday"),
    ("5", "Friday"),
    ("6", "Saturday"),
    ("7", "Sunday"),
    )
    
    notification = models.BooleanField(default=False, null=True)
    frequency = models.CharField(max_length=20, choices=FREQUENCY, default="Weekly")
    time = models.TimeField(null=True)
    day = models.DateField(null=True)


class StoreInfo(models.Model):
    telephone=models.CharField(max_length=11, null=True)
    email = models.EmailField(max_length=150, null=True, unique=True)
    address=models.CharField(max_length=50, null=True)

    def __str__(self) -> str:
        return f'FacMaSys'
    