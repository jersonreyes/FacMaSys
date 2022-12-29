from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Feeds(models.Model):
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  subject = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  date_created = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(default='profile_icon.png', upload_to='Announcements')
  link = models.CharField(max_length=200, default="N/A")
  
  def __str__(self) -> str:
    return f'ID: {self.user_id} | {self.subject}'