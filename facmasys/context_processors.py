from django.conf import settings
from django.http import HttpRequest


def theme(request):
    key = request.COOKIES.get('theme')
    return {'theme': key}
    
def ajax(request):
    is_ajax = False
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        is_ajax = True
    else:
        is_ajax = False
    return {'ajax': is_ajax}