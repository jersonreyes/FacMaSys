from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path('',views.index, name='researches-index'),
    path('selector',views.selector, name='selector-index'),
    path('get/<int:id>',views.get_research, name="researches-get"),
]
