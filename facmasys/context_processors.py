from django.conf import settings


def theme(request):
    key = request.COOKIES.get('theme')
    return {'theme': key}
    