import django_tables2 as tables

from .models import ActivityLog


class ActivityTable(tables.Table):
     user = tables.Column(accessor='user__username')
     class Meta:
         model = ActivityLog
         template_name = "partials/bootstrap_htmx_table.html"
