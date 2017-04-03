import pandas as pd
import numpy as np
import traceback
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *

def parse(a):
    file = '/var/www/gismap/room_mapping.csv'
    df = pd.read_csv(file)
    df = df.fillna("")
    school= School.objects.get(Name = "Andover High School")

    rooms = []
    non_rooms = []

    for i in range(1, len(df['Old Number']) + 1):
        new_room_number = df._slice(slice(i - 1, i))['New Number']
        old_room_number = df._slice(slice(i - 1, i))['Old Number']
        new_number = str(new_room_number)
        old_number = str(old_room_number)
        new_number = new_number[new_number.index("   " ) + 4: new_number.index('\n')]
        type = old_number[old_number.index("(") + 1: old_number.index(")")]
        old_number = old_number[old_number.index("   ") + 4: old_number.index("(") - 1]
        room = Room (Name = new_number, OldName = old_number, Type = type, School = school)

        try:
            if ('-' in new_number):
                new_number = new_number[0:new_number.index("-")]

            int(new_number)
            if (len(rooms) == 0):
                rooms.append(room)
            else:

                for j in range(0, len(rooms)):
                    if ('-' in rooms[j].Name):
                        room_number = rooms[j].Name[0: rooms[j].Name.index("-")]
                    else:
                        room_number = rooms[j].Name
                    if int(new_number) < int(room_number):
                        rooms.append(Room(Name = None, OldName = None))
                        rooms[j + 1:len(rooms)] = rooms[j:len(rooms) - 1]
                        rooms[j] = room
                        break
                    elif int(new_number) == int(room_number):
                        rooms.append(Room(None))
                        rooms[j + 2:len(rooms)] = rooms[j + 1:len(rooms) - 1]
                        rooms[j + 1] = room
                        break
                    if j == len(rooms) - 1:
                        rooms.append(room)

        except ValueError:

            non_rooms.append(room)
    for i in range(0, len(rooms)):
        rooms[i].save()

    for i in range (0, len(non_rooms)):
        non_rooms[i].save()





a = ""
#parse(a)
