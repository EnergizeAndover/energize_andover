import pandas as pd
import numpy as np
import traceback
import re
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *

def parse(file, school):

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
        circs = Circuit.objects.filter(FQN = fqn).filter(School=school)
        circuit = circs.first()

        #print (circuit)
        try:
            if len(circuit.Name) > 0:
                if (location != "skip"):
                    try:
                        if len(location) < 4:
                            rooms = Room.objects.filter(Name=location).filter(School = school)
                        else:
                            rooms = Room.objects.filter(OldName = location).filter(School = school)
                        room = rooms.first()
                        room.Panels.add(circuit.Panel)
                        room.save()
                        print("A")
                        circuit.Rooms.add(room)
                        devices = Device.objects.filter(Name=obj).filter(School = school)
                        print ("B")
                        if (not tf or str(devices) == "<QuerySet []>"):
                            device = Device(Name=obj, Power="NA", Location="None", Room=room, Number=i, School = school)
                            device.save()
                            devices = Device.objects.filter(Number=i).filter(School = school)
                        device = devices.first()
                        device.Circuit.add(circuit)

                        device.save()
                        #print ("yo")

                    except Exception as e:
                        print(e)
                        try:
                            device = Device.objects.filter(School=school).get(Name=obj)
                        except:
                            if tf:
                                device = Device(Name=obj, Power="NA", Location="None", Number=i, School = school)
                                device.save()
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