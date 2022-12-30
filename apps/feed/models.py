from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Feeds(models.Model):
  TYPE = (
    ('Deparment Head', 'Deparment Head'),
    ('Research Coordinator', 'Research Coordinator'),
    ('Extension Coordinator', 'Extension Coordinator'),
  )
  user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  subject = models.CharField(max_length=200)
  description = models.CharField(max_length=200)
  date_created = models.DateTimeField(auto_now_add=True)
  image = models.ImageField(default='profile_icon.png', upload_to='Announcements')
  link = models.CharField(max_length=200, default="N/A")
  user_type = models.CharField(choices=TYPE, max_length=100, default='Deparment Head')
  
  
  def __str__(self) -> str:
    return f'ID: {self.user_id} | {self.subject}'
  
class Feeds_DepartmentHead(models.Model):
  AGENDA = (
    ('Urgent', 'Urgent'),
    ('Just In', 'Just In'),
    ('Important', 'Important'),
    ('Emergency', 'Emergency'),
    ('Acknowledgements', 'Acknowledgements'),
    ('FYI', 'FYI'),
    ('Event', 'Event'),
    ('News', 'News'),
    ('Greetings', 'Greetings'),
    ('Others', 'Others'),
  )
  
  reference_id = models.OneToOneField(Feeds, on_delete=models.CASCADE)
  # issued_by = models.CharField(max_length=200)
  agenda = models.CharField(choices=AGENDA, max_length=100, default='Greetings')
  


class Feeds_ResearchCoord(models.Model):
  AGENDA = (
    ('On Call Papers', 'On Call Papers'),
    ('Journal Publication', 'Journal Publication'),
    ('Special Issues', 'Special Issues'),
    ('Intellectual Property Rights', 'Intellectual Property Rights'),
    ('Preparation of Instructional Materials', 'Preparation of Instructional Materials'),
    ('Revision of Research Guidelines', 'Revision of Research Guidelines'),
    ('Acknowledgement of Research Guidelines', 'Acknowledgement of Research Guidelines'),
    ('Research and Innovation', 'Research and Innovation'),
    ('Others', 'Others'),
  )
  
  reference_id = models.OneToOneField(Feeds, on_delete=models.CASCADE)
  # issued_by = models.CharField(max_length=200)
  deadline_start = models.DateField()
  deadline_end = models.DateField()
  agenda = models.CharField(choices=AGENDA, max_length=100, default='On Call Papers')


class Feeds_ExtensionCoord(models.Model):
  AGENDA = (
    ('On Call Papers', 'On Call Papers'),
    ('Signing of MOA', 'Signing of MOA'),
    ('Discussion of MOA', 'Discussion of MOA'),
    ('Partnership Programs', 'Partnership Programs'),
    ('Development Programs', 'Development Programs'),
    ('Extension Projects', 'Extension Projects'),
    ('Camp Projects', 'Camp Projects'),
    ('College Accreditation', 'College Accreditation'),
    ('Others', 'Others'),
  )
  
  reference_id = models.OneToOneField(Feeds, on_delete=models.CASCADE)
  # issued_by = models.CharField(max_length=200)
  # email = models.CharField(max_length=100)
  # extension_address = models.CharField(max_length=200)
  event_date = models.DateField()
  agenda = models.CharField(choices=AGENDA, max_length=100, default='On Call Papers')
  