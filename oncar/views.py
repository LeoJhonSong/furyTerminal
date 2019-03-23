from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Speed

max_speed = 80

def index(request):
    current_speed = Speed.objects.order_by('-speed_time')[0].speed_value
    context = {
        'current_speed': current_speed,
        'max_speed': max_speed
    }
    return render(request, 'oncar/index.html', context)

def refresh(request):
    data = {
        'current_speed': Speed.objects.order_by('-speed_time')[0].speed_value,
        'max_speed': max_speed
    }
    return JsonResponse(data)
