import django_tables2 as tables
from django.contrib.auth.models import User


class FacultyTable(tables.Table):
    phone = tables.Column(accessor='profile__phone')
    
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
        sequence = ('first_name','last_name','username','email','phone','action')
        template_name = "partials/bootstrap_htmx_table.html"