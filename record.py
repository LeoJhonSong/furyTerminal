#! /usr/bin/env python3

# record data from CAN Bus to the database

# TODO: maybe asyncio is needed, to pass data to oncar/views.py

import os
import time
import datetime

import furyCAN.bus

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'furyTerminal.settings')
django.setup()
from oncar.models import State

while True:
    can1 = furyCAN.bus.CAN()
    switch = 0
    last = time.time()
    # to collect all state data, read for a while
    while time.time() - last < 0.2:
        id, data = can1.decode()
        can1.read(id, data)
        switch = 1
    # **can1.state allow us to pass this dict as a argument list to the function
    if switch:
        State.objects.create(**can1.state)
        print(datetime.datetime.now())
        # State.objects.create(speed=datetime.datetime.now().second)
    can1.bus.shutdown()
