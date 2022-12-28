from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Announcements(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  subject = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  date_created = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(default='profile_icon.png', upload_to='Announcements')
  link = models.CharField(max_length=200, default="N/A")
  
  def __str__(self) -> str:
    return f'ID: {self.user_id} | {self.subject}'