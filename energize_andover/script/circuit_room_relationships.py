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
    df = df.fillna("skip")
    for i in range(1, len(df['DeviceObj']) + 1):
        obj = str(df._slice(slice(i - 1, i))['DeviceObj'])
        fqn = str(df._slice(slice(i - 1, i))['Circuit'])
        location = str(df._slice(slice(i - 1, i))['Location'])
        if (obj is not "skip"):
            obj = obj[obj.index("   ") + 4: obj.index('\n')]
            fqn = fqn[fqn.index("   ") + 4: fqn.index('\n')]
            location = location[location.index("   ") + 4: location.index('\n')]

        print (fqn)
        #print (location)
        circuit = Circuit.objects.filter(FQN = fqn)
        #print (circuit)
        if len(circuit) > 0:
            #print (circuit[0].Panel)
            if (location != "skip"):
                try:
                    if len(location) < 4:
                        room = Room.objects.filter(Name=location)
                    else:
                        room = Room.objects.filter(OldName = location)
                    print(room)
                    room[0].Panels.add(circuit[0].Panel)
                    room[0].save()
                    circuit[0].Rooms.add(room[0])
                except:
                    None
            circuit[0].Function = obj
            circuit[0].save()
a = ""
#parse(a)