from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    return render(request, 'home/index.html', {'state':'home'})
    
from django.shortcuts import get_object_or_404, render


def page_not_found(request, exception):
    return render(request, '404.html', status=404)
    
def permission_denied(request, exception):
    return render(request, '403.html', status=403)

def bad_request(request, exception):
    return render(request, '400.html', status=400)

def server_error(request, *args, **argv):
    return render(request, '500.html', status=500)