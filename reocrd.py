#! /usr/bin/env python3

# record data from CAN Bus to the database

# TODO: maybe asyncio is needed, to pass data to oncar/views.py

import os
import time

import furyCAN.bus

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furyTerminal.settings')
django.setup()
from oncar.models import State

can1 = furyCAN.bus.CAN()
while True:
    id, data = can1.decode()
    can1.read(id, data)
    # **can1.state allow us to pass this dict as a argument list to the function
    State.objects.create(**can1.state)
    # refresh period (s)
    time.sleep(0.05)
