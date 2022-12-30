import django_tables2 as tables
from django.contrib.auth.models import User


class FacultyTable(tables.Table):
    phone = tables.Column(accessor='profile__phone')
    department = tables.Column(accessor='profile__spec_track')
    
    action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} 
                <span class="tooltips_top"> 
                    <a class="form-modal-toggler bg-transparent border-0 text-black dark:white hover:main-theme font-bold dropdown-item p-2" title="View Staff" href="{% url 'faculty-index-detail' record.id %}">
                        <div class="gap-2 flex items-center">
                            <span class="tooltiptext_top">View Staff</span><img src="{% static 'images/icon_view.png' %}" class="invert dark:invert-0" style="width:18px; height:18px;" alt="View Staff">
                        </div>
                    </a>
                </span>
                {% if request.user.profile.user_role == 'depthead' or request.user.is_superuser %}
                <span class="tooltips_top"> 
                    <button onclick="window.location.href = '{% url 'faculty-add-dept' record.id %}'" class="bg-transparent border-0 text-black dark:white hover:main-theme font-bold dropdown-item p-2" title="Add to my dept.">
                        <div class="gap-2 flex items-center">
                            <span class="tooltiptext_top">Add to my Department</span><img src="{% static 'images/icon_view.png' %}" class="invert dark:invert-0" style="width:18px; height:18px;" alt="Add to my Dept.">
                        </div>
                    </button>
                </span>
                <span class="tooltips_top"> 
                    <a class="form-modal-toggler bg-transparent border-0 text-black dark:white hover:main-theme font-bold dropdown-item p-2" title="Add Handled Subject/s" href="{% url 'faculty-add-subjects' record.id %}">
                        <div class="gap-2 flex items-center">
                            <span class="tooltiptext_top">Add Handled Subject/s</span><img src="{% static 'images/icon_view.png' %}" class="invert dark:invert-0" style="width:18px; height:18px;" alt="Add Handled Subject/s">
                        </div>
                    </a>
                </span>
                {% endif %}
                ''')
    
    class Meta:
        model = User
        exclude = ('id','password','last_login','is_superuser','is_staff','is_active','date_joined')
        verbose_name = 'Faculty'
        sequence = ('first_name','last_name','username','email','phone','department','action')
        template_name = "partials/bootstrap_htmx_table.html"
        

class FacultyWithResearchTable(tables.Table):
    phone = tables.Column(accessor='profile__phone')
    no_of_research = tables.Column(accessor='number_of_research')
    'faculty-add-dept'
    action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} 
                <span class="tooltips_top"> 
                    <a class="form-modal-toggler bg-transparent border-0 text-black dark:white hover:main-theme font-bold dropdown-item p-2" title="View Staff" href="{% url 'faculty-index-detail' record.id %}">
                        <div class="gap-2 flex items-center">
                            <span class="tooltiptext_top">View Staff</span><img src="{% static 'images/icon_view.png' %}" class="invert dark:invert-0" style="width:18px; height:18px;" alt="View Staff">
                        </div>
                    </a>
                </span>
                ''')
    
    class Meta:
        model = User
        exclude = ('id','password','last_login','is_superuser','is_staff','is_active','date_joined')
        verbose_name = 'Faculty'
        sequence = ('first_name','last_name','username','email','phone','no_of_research','action')
        template_name = "partials/bootstrap_htmx_table.html"
        
        
class FacultyWithExtensionTable(tables.Table):
    phone = tables.Column(accessor='profile__phone')
    no_of_extension = tables.Column(accessor='number_of_extension')
    
    action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} 
                <span class="tooltips_top"> 
                    <a class="form-modal-toggler bg-transparent border-0 text-black dark:white hover:main-theme font-bold dropdown-item p-2" title="View Staff" href="{% url 'faculty-index-detail' record.id %}">
                        <div class="gap-2 flex items-center">
                            <span class="tooltiptext_top">View Staff</span><img src="{% static 'images/icon_view.png' %}" class="invert dark:invert-0" style="width:18px; height:18px;" alt="View Staff">
                        </div>
                    </a>
                </span>
                ''')
    
    class Meta:
        model = User
        exclude = ('id','password','last_login','is_superuser','is_staff','is_active','date_joined')
        verbose_name = 'Faculty'
        sequence = ('first_name','last_name','username','email','phone','no_of_extension','action')
        template_name = "partials/bootstrap_htmx_table.html"