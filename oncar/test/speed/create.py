import sys
import os
import random
import time
import django
sys.path.append("../../../")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furyTerminal.settings')
django.setup()
from oncar.models import Speed
from furyTerminal import settings

Speed.objects.create(speed_value=sys.argv[1])

i = 0
max = 200
while(True):
    a = random.randint(-0.1*max, 0.1*max)
    while (i + a < 0) or (i + a > max):
        a = random.randint(-0.1*max, 0.1*max)
    i = i + a
    print(i)
    Speed.objects.create(speed_value=i)
    time.sleep(0.05)
