import json
import os
import socket

from django.http import JsonResponse
from django.shortcuts import render
from . import bus


def index(request):
    return render(request, 'oncar/index.html')


def devices(request):
    return render(request, 'oncar/devices/index.html')


def refresh(request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(('0.0.0.0', 8080))
    # s.send(b'Give me')
    state = eval(s.recv(1024).decode('utf-8'))
    data = {
        'speed': state['speed'] if 'speed' in state else 0,
        'power': state['power'] if 'power' in state else 0,
        'batSoc': state['batSoc'] if 'batSoc' in state else 0,
        'mcuTemp': state['mcuTemp'] if 'mcuTemp' in state else 0,
        'motorTemp': state['motorTemp'] if 'motorTemp' in state else 0,
        'batMaxTemp': state['batMaxTemp'] if 'batMaxTemp' in state else 0,
    }
    # s.send(b'exit')
    s.close()
    return JsonResponse(data)


def poweroff(request):
    os.system('sudo poweroff')
