from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('refresh', views.refresh, name='refresh'),
    path('poweroff', views.poweroff, name='poweroff'),
]
