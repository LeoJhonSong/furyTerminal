from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import State


def index(request):
    return render(request, 'oncar/index.html')


def refresh(request):
    data = {
        'speed': State.objects.order_by('-time_stamp')[0].speed,
    }
    return JsonResponse(data)
