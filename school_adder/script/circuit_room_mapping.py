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
            description = description[description.index("   ") + 4: description.index('\n')]
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
                        trans = Transformer(Name = path[s1: len (path)], FQN = path, Notes = description, School = school)
                        trans.save()
            if (type == "circuit"):
                #print ("circuit")
                num = path.count(".")
                if num == 1:
                    name = path
                    panel = path[0:path.index('.')]
                    number = path[path.index('.') + 1: len(path)]
                    s2 = path.index ('.')
                else:
                    count = 0
                    s1 = 0
                    s2 = 0
                    for j in range (0, len (path) - 1):
                        if path[j] is '.':
                            count += 1
                            if count == num - 1:
                                s1 = j
                            elif count == num:
                                s2 = j
                    panel = path[s1 + 1: s2]
                    name = path[s1 + 1:]
                    number = path[s2 + 1: len(path)]
                #print ("Circuit: Name: %s, Number: %s, Panel: %s, Rooms: %s," % (circuit, number, panel, rooms))

                try:
                    #print (path[0:s2])
                    panels_obj = Panel.objects.filter(FQN=path[0:s2]).filter(School = school)
                except:
                    panels_obj = None
                #for i in range (0, len(panels_obj)):
                    #print(panels_obj[i])
                circuit = Circuit(Name=name, Number=number, Panel=panels_obj.first(), FQN = path, School = school, Notes = description)
                circuit.save()

            if (type == 'panel'):
                #print ("panel")
                #print ("1")
                closet = None
                try:
                    Closet.objects.filter(School=school).get(Old_Name=room) == None
                except:
                    try:
                        #print ("3")
                        closet_name = Room.objects.filter(School=school).get(OldName=room).Name
                        closet = Closet(Name=closet_name, Old_Name=room, School=school)
                    except:
                        #print ("4")
                        closet = Closet(Name="NL", Old_Name=room, School=school)
                    closet.save()
                number = path.count('.')
                if number == 0:
                    name = path
                    closet = Closet.objects.filter(Old_Name = room).filter(School = school).first()
                    new_panel = Panel(Name = name, Voltage = voltage, Location = "None", Closet=closet, School = school, FQN = path, Notes = description)
                else:
                    count = 0
                    s1 = -1
                    s2 = 0
                    s3 = 0
                    summary_path = path
                    for j in range (0, len(transformer)):
                        if transformer[k] in summary_path:
                            summary_path = summary_path.replace (transformer[k], "")
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
                    name = summary_path[s3 + 1: len(path)]
                    panel = summary_path [s1 + 1: s2]

                #print ("Panel: Name: " + name + ", Voltage: " + voltage + "V, Location: None, School: AHS, Closet: " + room)

                    print(str(Closet.objects.filter(Old_Name = room).filter(School = school)))

                    try:
                        panel_objs = Panel.objects.filter(FQN = path[0:path.index(panel)] + panel).filter(School = school)
                        panel_obj = panel_objs[0]

                    except:
                        panel_obj = None
                    closet = Closet.objects.filter(Old_Name = room).filter(School = school).first()
                    new_panel = Panel(Name=name, Voltage=voltage, Location="None", Panels=panel_obj, School=school, Closet=closet, FQN = path, Notes = description)

                new_panel.save()


a = ''
#parse(a)