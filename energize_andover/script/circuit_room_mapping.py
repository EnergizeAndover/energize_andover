import pandas as pd
import numpy as np
import traceback
import re
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *

def parse(a):
    file = '/var/www/gismap/circuit_mapping_updated.csv'
    df = pd.read_csv(file)
    df = df.fillna("skip")
    school = (School.objects.get(Name="Andover High School"))
    transformer = []
    for i in range(1, len(df['path']) + 1):
        path = str(df._slice(slice(i - 1, i))['path'])
        type = str(df._slice(slice(i - 1, i))['type'])
        voltage = str(df._slice(slice(i - 1, i))['voltage'])
        room = str(df._slice(slice(i - 1, i))['room'])
        description = str(df._slice(slice(i - 1, i))['description'])
        if (path is not "skip"):
            type = str.lower(type[type.index("   ") + 4: type.index('\n')])
            path = path[path.index("   ") + 4: path.index('\n')]
            voltage = voltage[voltage.index("   ") + 4: voltage.index('\n')]
            room = room[room.index("   ") + 4: room.index('\n')]
            if ("transformer" in type):
                number = path.count('.')
                count = 0
                s1 = len(path)
                for j in range(0, len(path)):
                    if path[j] is '.':
                        count += 1
                        if count == number:
                            s1 = j
                    in_array = False
                    for k in range (0, len(transformer)):
                        if transformer[k] == path[s1: len (path)]:
                            in_array = True
                    if (not in_array):
                        transformer.append(path[s1: len (path)])
            if (type == "circuit"):
                print ("circuit")
                number = path.count(".")
                if number == 1:
                    name = path
                    panel = path[0:path.index('.')]
                else:
                    count = 0
                    s1 = 0
                    s2 = 0
                    for j in range (0, len (path) - 1):
                        if path[j] is '.':
                            count += 1
                            if count == number - 1:
                                s1 = j
                            elif count == number:
                                s2 = j
                    panel = path[s1 + 1: s2]
                    name = path[s1 + 1:]
                    circuit = path[s1 + 1: len(path)]
                    number = path[s2 + 1: len(path)]
                rooms = re.findall(r"\D(\d{4})\D", description)
                #print ("Circuit: Name: %s, Number: %s, Panel: %s, Rooms: %s," % (circuit, number, panel, rooms))

                try:
                    panels_obj = Panel.objects.filter(Name=panel)
                except:
                    panels_obj = None
                for i in range (0, len(panels_obj)):
                    print(panels_obj[i])
                circuit = Circuit(Name=name, Number=number, Panel=panels_obj[0], FQN = path)
                circuit.save()

            if (type == 'panel'):
                #print ("panel")
                number = path.count('.')
                if number == 0:
                    name = path
                else:
                    count = 0
                    s1 = -1
                    s2 = 0
                    s3 = 0
                    for j in range (0, len(transformer)):
                        if transformer[k] in path:
                            path = path.replace (transformer[k], "")
                            number-=1
                    for j in range(0, len(path) - 1):
                        if path[j] is '.':
                            count += 1
                            if count == number - 2:
                                s1 = j
                            if count == number - 1:
                                s2 = j
                            elif count == number:
                                s3 = j
                    name = path[s3 + 1: len(path)]
                    panel = path [s1 + 1: s2]

                #print ("Panel: Name: " + name + ", Voltage: " + voltage + "V, Location: None, School: AHS, Closet: " + room)
                print (str(Closet.objects.filter(Old_Name = room)))
                if str(Closet.objects.filter(Old_Name = room)) == '<QuerySet []>':
                    try:
                        closet = Closet (Name = Room.objects.get(OldName = room).Name, Old_Name = room, School = school)
                    except:
                        closet = Closet(Name = "NL", Old_Name=room, School=school)
                    closet.save()
                try:
                    panel_objs = Panel.objects.filter(Name = panel)
                    panel_obj = panel_objs[0]
                except:
                    panel_obj = None
                new_panel = Panel(Name=name, Voltage=voltage, Location="None", Panels=panel_obj, School=school, Closet=Closet.objects.filter(Old_Name = room)[0], FQN = path)
                add = True
                """
                for i in range (0, len(Panel.objects.all())):
                    #print(Panel.objects.all()[i].Name)
                    if Panel.objects.all()[i].Name == name:
                        add = False
                        break
                if (add):"""
                new_panel.save()


a = ''
#parse(a)