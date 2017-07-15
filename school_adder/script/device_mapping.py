import pandas as pd
import numpy as np
import traceback
import re
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *

def parse(file, school):
    df = pd.read_csv(file)
    df = df.fillna("skip")
    transformer = []
    for i in range(1, len(df['Device']) + 1):
        device = str(df._slice(slice(i - 1, i))['Device'])
        associated_device = str(df._slice(slice(i - 1, i))['Associated Device'])
        power = str(df._slice(slice(i - 1, i))['Power'])
        zone = str(df._slice(slice(i - 1, i))['Zone'])
        device = device[device.index("   ") + 4: device.index('\n')]
        associated_device = associated_device[associated_device.index("   ") + 4: associated_device.index('\n')]
        power = power[power.index("   ") + 4: power.index('\n')]
        zone = zone[zone.index("   ") + 4: zone.index('\n')]
        #print(Device.objects.filter(School = school).get(Name="AHU-1").Name)
        try:
            dev = Device.objects.filter(School = school).get(Name = device)
            if not dev is None:
                try:
                    assoc_dev = Device.objects.filter(School = school).get(Name = associated_device)
                    if not assoc_dev is None:
                        dev.Associated_Devices.add(assoc_dev)
                        assoc_dev.Associated_Devices.add(dev)
                        assoc_dev.save()
                except:
                    None
                dev.Power = power
                dev.Location = zone
                dev.save()
        except:
            None