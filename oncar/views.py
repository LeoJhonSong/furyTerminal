import json
import os

from django.http import JsonResponse
from django.shortcuts import render

from .models import State


def index(request):
    return render(request, 'oncar/index.html')


def refresh(request):
    latest = State.objects.order_by('-time_stamp')[0]
    data = {
        'speed': latest.speed,
        'power': latest.power,
        'batSoc': latest.batSoc,
        'mcuTemp': latest.mcuTemp,
        'motorTemp': latest.motorTemp,
        'batMaxTemp': latest.batMaxTemp,
    }
    return JsonResponse(data)


def poweroff(request):
    os.system('poweroff')
