from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

"""
WAG KALIMUTANG LAGYAN SI URLS.PY NG PATH DOON SA MAIN PROJECT!!!!
"""


# Create your models here.

""" ################################# EXTENSIONS ################################# """
class ExtensionService_Collaborators(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    # academe = models.CharField(max_length=200)

class ExtensionService_OfferedPrograms(models.Model):
    program_name = models.CharField(max_length=200)
    description = models.TextField(max_length=200, null=True, blank=True)
    # academe = models.CharField(max_length=200) 

class ExtensionService(models.Model):
    faculty_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=200)
    logo = models.ImageField(default=None, upload_to='extension_service_profilepic/', blank=True, null=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True, unique=True)
    contact_no = models.CharField(max_length=15, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)
    background = models.TextField(max_length=500)
    extension_head = models.CharField(max_length=200, null=True, blank=True)
    ext_offeredprograms_id = models.ForeignKey(ExtensionService_OfferedPrograms, on_delete=models.CASCADE, blank=True, null=True)
    ext_collaborator_id = models.ForeignKey(ExtensionService_Collaborators, on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self) -> str:
        return f'Name: {self.name} | Website: {self.website}'


""" ################################# RESEARCH ################################# """
class Research(models.Model):
    RESEARCH_PROGRESS = (
        ('Ongoing', 'Ongoing'),
        ('Presented', 'Presented'),
        ('Published', 'Published'),
    )
    
    RESEARCH_AREA = (
        ('Algorithms and Theory', 'Algorithms and Theory'),
        ('Data Management', 'Data Management'),
        ('Data Mining and Modeling', 'Data Mining and Modeling'),
        ('Distributed Systems and Parallel Computing', 'Distributed Systems and Parallel Computing'),
        ('Economics and Electronic Commerce', 'Economics and Electronic Commerce'),
        ('Education Innovation', 'Education Innovation'),
        ('General Science', 'General Science'),
        ('Health & Bioscience', 'Health & Bioscience'),
        ('Hardware and Architecture', 'Hardware and Architecture'),
        ('Human-Computer Interaction and Visualization', 'Human-Computer Interaction and Visualization'),
        ('Information Retrieval and the Web', 'Information Retrieval and the Web'),
        ('Machine Intelligence', 'Machine Intelligence'),
        ('Machine Perception', 'Machine Perception'),
        ('Machine Translation', 'Machine Translation'),
        ('Mobile Systems', 'Mobile Systems'),
        ('Natural Language Processing', 'Natural Language Processing'), 
        ('Networking', 'Networking'),
        ('Quantum Computing', 'Quantum Computing'),
        ('Robotics', 'Robotics'),
        ('Security, Privacy and Abuse Prevention', 'Security, Privacy and Abuse Prevention'),
        ('Software Engineering', 'Software Engineering'),
        ('Software Systems', 'Software Systems'),
        ('Speech Processing', 'Speech Processing'),
        ('Others', 'Others'),
    )
    
    DEGREE_LEVEL = (
        ("Associate Degree", "Associate Degree"), 
        ("Bachelor Degree", "Bachelor Degree"),
        ("Masters Degree", "Masters Degree"),
        ("Doctorate Degree", "Doctorate Degree"),
        ("Independent", "Independent"),
    )
    
    CONTENT_TYPE = (
        ('Journal', 'Journal'),
        ('Article', 'Article'),
        ('Magazines', 'Magazines'),
        ('Reviews', 'Reviews'),
        ('Conference Paper', 'Conference Paper'),
        ('Technical Reports', 'Technical Reports'),
    )
    
    # faculty_id = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    # extension_service_id = models.ForeignKey(ExtensionService, on_delete=models.CASCADE)
    faculty_id = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    research_title = models.CharField(max_length=100, blank=False, null=False)
    research_progress = models.CharField(max_length=100, choices=RESEARCH_PROGRESS, blank=False, null=False, default=None)
    research_area = models.CharField(max_length=100, choices=RESEARCH_AREA, blank=True, null=True, default=None)
    degree_level = models.CharField(max_length=100, choices=DEGREE_LEVEL, blank=True, null=True, default=None)
    abstract = models.CharField(max_length=1500, blank=True, null=True, default=None)
    content_type = models.CharField(max_length=100, choices=CONTENT_TYPE, blank=True, null=True, default="Journal")
    date_added = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    document = models.FileField(upload_to='Researches/', blank=True, null=True, default=None)
    researcher_school = models.CharField(max_length=100, blank=False, null=False)
    # presented_id = models.ForeignKey(Research_Presented, on_delete=models.CASCADE, blank=True, null=True)
    # published_id = models.ForeignKey(Research_Published, on_delete=models.CASCADE, blank=True, null=True)

    # models.OneToOneField(User, on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        # return f'Research Title: {self.research_title} | Research Progress: {self.research_progress} | Degree Level: {self.degree_level}'
        return f'Research Title: {self.research_title}'
    
    def __references__(self):
        return self.faculty_id



class Research_Presented(models.Model):
    PRESENTATION = (
        ("Physical", "Physical"),
        ("Virtual", "Virtual"),
        ("Hyrbrid", "Hyrbrid"),
    )
    
    EVENT_TYPE = (
        ('Conference', 'Conference'),
        ("Seminars", "Seminars"),
        ("Product Launch", "Product Launch"),
        ("Corporate / Executive Meetings", "Corporate / Executive Meetings"),
        ("Summits", "Summits"),
        ("Symposium", "Symposium"),
        ("Trade Shows", "Trade Shows"),
        ("Others", "Others"),
    )
    
    short_name = models.CharField(max_length=50, null=False, blank=False)
    event_name = models.CharField(max_length=200, null=False, blank=False)
    event_venue = models.CharField(max_length=200, null=False, blank=False)
    event_start_date = models.DateField(null=False, blank=False)
    event_end_date = models.DateField(null=False, blank=False)
    presentation_type = models.CharField(max_length=200, choices=PRESENTATION, default="Conference", blank=False, null=True)
    event_type = models.CharField(max_length=200, choices=EVENT_TYPE, default="Physical", blank=False, null=True)
    org_name = models.CharField(max_length=200, null=False, blank=False)
    org_website_url = models.CharField(max_length=200, null=False, blank=False)
    org_support = models.CharField(max_length=200, null=False, blank=False)
    org_description = models.TextField(max_length=500, null=False, blank=False)
    date_presented = models.DateField(null=False)
    presented_id = models.OneToOneField(Research, on_delete=models.CASCADE, blank=True, null=True)
    faculty_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    
    def __str__(self) -> str:
        return f'{self.presented_id} {self.short_name}: {self.event_name}, {self.date_presented}'
    


class Research_Published(models.Model):
    RESEARCH_LICENSE = (
        ("Creative Commons Licenses", "Creative Commons Licenses"), 
        ("Alternatives Publishing Licenses", "Alternatives Publishing Licenses"),
        ("Research Repository Licences", "Research Repository Licences"),
        ("Open Access", "Open Access"),
        ("None", "None"),
    )
    
    
    published_date = models.DateField(null=False)
    publication = models.CharField(max_length=200, blank=False, null=False)
    source = models.CharField(max_length=200, blank=False, null=False)
    research_license = models.CharField(max_length=200, choices=RESEARCH_LICENSE, default="None", blank=False, null=True)
    abstract = models.TextField(max_length=1200, blank=False, null=False)
    published_id = models.OneToOneField(Research, on_delete=models.CASCADE, blank=True, null=True)
    faculty_id = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)

    def __str__(self) -> str:
        return f'{self.published_id} {self.publication}: {self.published_date}, {self.research_license}'
    




""" ################################# SUBJECTS ################################# """
class Subjects(models.Model):
    SEMESTERS = (("1st Semester", "1st Semester"), ("2nd Semester", "2nd Semester"))
    SPECIALIZATIONS = (
        ("Service Management Specialization Track", "Service Management Specialization Track"),
        ("Business Analytics Specialization Track", "Business Analytics Specialization Track"),
        ("Web and Mobile Application Specialization Track", "Web and Mobile Application Specialization Track"),
        ("None", "None"),
    )
    COURSES_TYPE = (
        ("General Education Courses", "General Education Courses"),
        ("Common Courses", "Common Courses"),
        ("Professional Courses", "Professional Courses"),
        ("Professional Electives", "Professional Electives"),
        ("Physical Education", "Physical Education"),
        ("National Service Training Program", "National Service Training Program"),
        ("None", "None"),
    )
    YEAR = (
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
    )
    
    course_code = models.CharField(max_length=20, blank=False, null=False, default="NSTP10")
    course_title = models.CharField(max_length=100, blank=False, null=False, default="National Service Training Program 1")
    course_credits = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=3)
    semester = models.CharField(max_length=50, choices=SEMESTERS, blank=False, default="1st Semester")
    year = models.CharField(max_length=50, choices=YEAR, blank=False, default=1)
    course_lec_units = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)], default=3)
    course_lab_units = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(24)], default=0)
    course_hours_per_week = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(1000)], default=3)
    specialization = models.CharField(max_length=50, choices=SPECIALIZATIONS, blank=True, null=True, default="None")
    pre_requisite = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None)
    course_type = models.CharField(max_length=50, choices=COURSES_TYPE, blank=False, default="None")
    
    def __str__(self) -> str:
        return f'{self.course_code} | Title: {self.course_title} | Credits: {self.course_credits}'


class Subjects_Taught(models.Model):
    faculty_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    handled_subjects =  models.ManyToManyField(Subjects)
    
    def __str__(self) -> str:
        return f'Faculty ID: {self.faculty_id} | Handled Subjects: {self.handled_subjects.values().all()}'


    
    