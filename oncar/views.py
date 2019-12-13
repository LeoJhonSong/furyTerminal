import json
import os

from django.http import JsonResponse
from django.shortcuts import render
from ..furyCAN import bus


def index(request):
    return render(request, 'oncar/index.html')


def devices(request):
    return render(request, 'oncar/devices/index.html')


stateCache = {}


def refresh(request):
    can1 = bus.CAN()
    global stateCache
    can1.state = stateCache
    id, data = can1.decode()
    can1.read(id, data)
    data = {
        'speed': can1.state['speed'],
        'power': can1.state['power'],
        'batSoc': can1.state['batSoc'],
        'mcuTemp': can1.state['mcuTemp'],
        'motorTemp': can1.state['motorTemp'],
        'batMaxTemp': can1.state['batMaxTemp'],
    }
    stateCache = can1.state
    can1.bus.shutdown()
    return JsonResponse(data)


def poweroff(request):
    os.system('sudo poweroff')
