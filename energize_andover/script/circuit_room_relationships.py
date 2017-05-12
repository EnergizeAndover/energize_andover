import pandas as pd
import numpy as np
import traceback
import re
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *

def parse(a):
    file = '/var/www/gismap/devices.csv'
    df = pd.read_csv(file)
    #df = df.fillna("skip")

    for i in range(1, len(df['DeviceObj']) + 1):
        obj = str(df._slice(slice(i - 1, i))['DeviceObj'])
        fqn = str(df._slice(slice(i - 1, i))['Circuit'])
        location = str(df._slice(slice(i - 1, i))['Location'])
        three_phase = str(df._slice(slice(i - 1, i))['Three Phase'])
        if (obj is not "skip"):
            obj = obj[obj.index("   ") + 4: obj.index('\n')]
            fqn = fqn[fqn.index("   ") + 4: fqn.index('\n')]
            location = location[location.index("   ") + 4: location.index('\n')]
            three_phase = three_phase[three_phase.index("   ") + 4: three_phase.index('\n')]
        tf = False
        if (three_phase == 'X'):
            tf = True
        print (fqn)
        #print (location)
        circ = Circuit.objects.filter(FQN = fqn)
        #print (circ)
        circuit = circ.first()

        #print (circuit)
        try:
            if len(circuit.Name) > 0:
                if (location != "skip"):
                    try:
                        if len(location) < 4:
                            rooms = Room.objects.filter(Name=location)
                        else:
                            rooms = Room.objects.filter(OldName = location)
                        room = rooms.first()
                        room.Panels.add(circuit.Panel)
                        room.save()
                        print("A")
                        circuit.Rooms.add(room)
                        dev = Device.objects.filter(Name=obj)
                        print ("B")
                        if (not tf or str(dev) == "<QuerySet []>"):
                            device = Device(Name=obj, Power="NA", Location="None", Room=room, Number=i)
                            device.save()
                            dev = Device.objects.filter(Number=i)
                        device = dev.first()
                        #print (device.Name)
                        device.Circuit.add(circuit)

                        device.save()
                        #print ("yo")

                    except Exception as e:
                        print(e)
                        dev = Device.objects.filter(Name=obj)
                        if (not tf or str(dev) == "<QuerySet []>"):
                            device = Device(Name=obj, Power="NA", Location="None", Number=i)
                            device.save()
                            dev = Device.objects.filter(Number=i)
                        device = dev.first()
                        print ("a")
                        device.Circuit.add(circuit)
                        device.save()
                        print ("b")

            circuit.Function = obj
            circuit.save()
        except Exception as e:
            None
a = ""
#parse(a)