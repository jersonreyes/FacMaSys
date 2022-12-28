from django.contrib.auth.models import User
from django.db import models


# class ActivityLog(models.Model):
#     datetime = models.DateTimeField(auto_now_add=True)
#     type = models.CharField(max_length=50, null=True)
#     location = models.CharField(max_length=50, null=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
#     message = models.CharField(max_length=255, null=True, blank=True)
    
#     def __str__(self) -> str:
#         return f'{self.type} {self.location}'
    
#     class Meta:
#         ordering = ('-datetime',)
     
        
class Notifications(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(max_length=255, null=True)
    read = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        return f'{self.user.username} : {self.message}'
    
    class Meta:
        ordering = ('-date',)
    