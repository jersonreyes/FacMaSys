from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    return render(request, 'home/index.html', {'state':'home'})
    