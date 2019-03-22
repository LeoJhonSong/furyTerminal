from django.shortcuts import render
from .models import Speed


def index(request):
    current_speed = Speed.objects.order_by('-speed_time')[0].speed_value
    context = {
        'current_speed': current_speed
    }
    return render(request, 'oncar/index.html', context)
