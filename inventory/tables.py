import django_tables2 as tables
from django.utils.html import format_html

from .models import Car, CarArchive, Service, ServiceArchive, Supplier, SupplierArchive, Shipment, ShipmentArchive


class ImageColumn(tables.Column):
  def render(self, value):
    return format_html('<img src="/media/{}" width="40" height="40"/>', value)
  
class CurrencyColumn(tables.Column):
  def render(self,value):
    return f'₱ {value:,}'


class ProductTable(tables.Table):
  images = ImageColumn(exclude_from_export=True)
  id = tables.Column()
  title = tables.Column()
  vendor = tables.Column()
  product_type = tables.Column()
  tags = tables.Column()
  price = CurrencyColumn()
  quantity = tables.Column()


class ServiceTable(tables.Table):
  image = ImageColumn(exclude_from_export=True)
  labor = CurrencyColumn()
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <span class="tooltips_top">
              <a class="btn btn-dark btn-sm pb-1" href="{% url 'inventory-service-update' record.id %}">
              <span class="tooltiptext_top"> Update Service </span> 
              <img src="{% static 'images/icon_update.png' %}" style="width:18px; height:18px;" alt="Update Service">
              </a>
            </span>
            
            <span class="tooltips_top">
              <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-service-archive' record.id %}">
              <button class="btn btn-danger btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.name }}','ARCHIVE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Archive </span> 
                <img src="{% static 'images/icon_archive.png' %}" style="width:18px; height:18px;" alt="Archive">
              </button>
            </span> 
            {% endif %}''')
  
  def before_render(self, request):
    if request.user.is_staff:
        self.columns.show('action')
    else:
        self.columns.hide('action')
  
  class Meta:
      model = Service
      exclude = ('id',)
      sequence = ('image',)
      template_name = "partials/bootstrap_htmx_table.html"
      abstract = True


class ServiceArchiveTable(ServiceTable):
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-service-restore' record.id %}">
            <span class="tooltips_top">
              <button class="btn btn-primary btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.name }}','RESTORE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Restore </span> 
                <img src="{% static 'images/icon_restore.png' %}" style="width:18px; height:18px;" alt="Restore">
              </button>
            </span>
            {% endif %}''')
  
  class Meta(ServiceTable.Meta):
    model = ServiceArchive


class CarTable(tables.Table):
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <span class="tooltips_top">
              <a class="btn btn-dark btn-sm pb-1" href="{% url 'inventory-car-update' record.id %}">
              <span class="tooltiptext_top"> Update Car </span> 
              <img src="{% static 'images/icon_update.png' %}" style="width:18px; height:18px;" alt="Update Car">
              </a>
            </span>
            
            <span class="tooltips_top">
              <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-car-archive' record.id %}">
              <button class="btn btn-danger btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.make }} {{ record.model }} {{ record.sub_model }} {{ record.year }}','ARCHIVE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Archive </span> 
                <img src="{% static 'images/icon_archive.png' %}" style="width:18px; height:18px;" alt="Archive">
              </button>
            </span> 
            {% endif %}''')
  
  class Meta:
      model = Car
      exclude = ('id',)
      template_name = "partials/bootstrap_htmx_table.html"
      abstract = True


class CarArchiveTable(CarTable):
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-car-restore' record.id %}">
            <span class="tooltips_top">
              <button class="btn btn-primary btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.make }} {{ record.model }} {{ record.sub_model }} {{ record.year }}','RESTORE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Restore </span> 
                <img src="{% static 'images/icon_restore.png' %}" style="width:18px; height:18px;" alt="Restore">
              </button>
            </span>
            {% endif %}''')
  
  class Meta(CarTable.Meta):
    model = CarArchive


class SupplierTable(tables.Table):
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <span class="tooltips_top">
              <a class="btn btn-dark btn-sm pb-1" href="{% url 'inventory-supplier-update' record.id %}">
              <span class="tooltiptext_top"> Update Supplier </span> 
              <img src="{% static 'images/icon_update.png' %}" style="width:18px; height:18px;" alt="Update Supplier">
              </a>
            </span>
            
            <span class="tooltips_top">
              <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-supplier-archive' record.id %}">
              <button class="btn btn-danger btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.name }}','ARCHIVE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Archive </span> 
                <img src="{% static 'images/icon_archive.png' %}" style="width:18px; height:18px;" alt="Archive">
              </button>
            </span> 
            {% endif %}''')
  
  class Meta:
      model = Supplier
      exclude = ('id',)
      template_name = "partials/bootstrap_htmx_table.html"
      abstract = True


class SupplierArchiveTable(SupplierTable):
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-supplier-restore' record.id %}">
            <span class="tooltips_top">
              <button class="btn btn-primary btn-sm pb-1" onclick="confirm({{ record.id }}, '{{ record.name }}','RESTORE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Restore </span> 
                <img src="{% static 'images/icon_restore.png' %}" style="width:18px; height:18px;" alt="Restore">
              </button>
            </span>
            {% endif %}''')
  
  class Meta(SupplierTable.Meta):
    model = SupplierArchive


class ShipmentTable(tables.Table):
  supplier = tables.Column(accessor='supplier__name',verbose_name='Supplier')
  base_price = CurrencyColumn()
  fees = CurrencyColumn()
  gross_amount = CurrencyColumn()
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-shipment-archive' record.id %}">
            <span class="tooltips_top">
              <button class="btn btn-danger btn-sm pb-1" onclick="confirm({{ record.id }}, 'Shipment ID: {{ record.id }}','ARCHIVE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Archive </span> 
                <img src="{% static 'images/icon_archive.png' %}" style="width:18px; height:18px;" alt="Archive">
              </button>
            </span>
            {% endif %}''')
  
  class Meta:
      model = Shipment
      sequence = ('id','date')
      template_name = "partials/bootstrap_htmx_table.html"
      abstract = True
      
        
class ShipmentArchivedTable(ShipmentTable):
  action = tables.TemplateColumn(exclude_from_export=True,template_code='''{% load static %} {% if user.is_staff %}
            <input type="hidden" id="link{{ record.id }}" value="{% url 'inventory-shipment-restore' record.id %}">
            <span class="tooltips_top">
              <button class="btn btn-primary btn-sm pb-1" onclick="confirm({{ record.id }}, 'Shipment ID: {{ record.id }}','RESTORE')" data-toggle="modal" data-target="#confirmModal">
                <span class="tooltiptext_top"> Restore </span> 
                <img src="{% static 'images/icon_restore.png' %}" style="width:18px; height:18px;" alt="Restore">
              </button>
            </span>
            {% endif %}''')
  
  class Meta(ShipmentTable.Meta):
    model = ShipmentArchive