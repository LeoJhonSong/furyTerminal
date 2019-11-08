from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import State


def index(request):
    return render(request, 'oncar/index.html')


def refresh(request):
    data = {
        'speed': State.objects.order_by('-time_stamp')[0].speed,
        'power': State.objects.order_by('-time_stamp')[0].power,
        'batSoc': State.objects.order_by('-time_stamp')[0].batSoc,
        'mcuTemp': State.objects.order_by('-time_stamp')[0].mcuTemp,
        'motorTemp': State.objects.order_by('-time_stamp')[0].motorTemp,
        'batMaxTemp': State.objects.order_by('-time_stamp')[0].batMaxTemp,
    }
    return JsonResponse(data)
