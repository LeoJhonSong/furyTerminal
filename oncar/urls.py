from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('devices', views.devices, name='devices'),
    path('refresh', views.refresh, name='refresh'),
    path('poweroff', views.poweroff, name='poweroff'),
]
