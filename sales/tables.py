import django_tables2 as tables
from django.utils.html import format_html

from .models import Order


class SalesTable(tables.Table):
    staff = tables.Column(accessor='staff__username',verbose_name='Staff')
    customer = tables.Column(accessor='customer__name',verbose_name='Customer')
    vat = tables.Column(verbose_name='VAT (12%)')
    pay_method = tables.Column(verbose_name='Payment method')
    pay_id = tables.Column(verbose_name='Payment Reference Number')
    action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <span class="tooltips_top">
              <a class="btn btn-dark btn-sm pb-1" href="{% url 'sales-customer-detail' record.id %}">
              <span class="tooltiptext_top"> View </span> 
              <img src="{% static 'images/icon_view.png' %}" style="width:18px; height:18px;" alt="View">
              </a>
            </span>
            {% if record.status != 'Returned' %}
            <span class="tooltips_top">
              <input type="hidden" id="link{{ record.id }}" value="{% url 'sales-return' record.id %}">
              <button class="btn btn-danger btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.invoice_number }}','RETURN')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Return </span> 
                <img src="{% static 'images/icon_archive.png' %}" style="width:18px; height:18px;" alt="Return">
              </button>
            </span>
            {% endif %}
            {% endif %}''')
    
    def before_render(self, request):
      if request.user.is_staff:
          self.columns.show('action')
      else:
          self.columns.hide('action')
  
    class Meta:
        model = Order
        exclude = ('id',)
        sequence = ('invoice_number','date_created','status','staff','customer','pay_method','pay_id','subtotal','vat','total','action')
        template_name = "partials/bootstrap_htmx_table.html"