from django.shortcuts import render
from energize_andover.models import *
import csv
import os
from datetime import datetime

def save_school (school, request):
    directory = ("school_" + school.Name + "_" + str(datetime.now())).replace(" ", "_")
    os.makedirs(directory)
    rooms = Room.objects.filter(School = school).order_by("id")
    file_name= (directory + "/" + "rooms_" + school.Name.lower() + "_" + str(datetime.now()) + ".csv").replace(" ", "_")
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Old Number', 'New Number', 'Extra Info', 'NL = Not Labeled'])
        for room in rooms:
            writer.writerow([room.OldName +" (" + room.Type + ")", room.Name,"",""])
    file_name= file_name.replace("rooms", "panels")
    panels = Panel.objects.filter(School= school).order_by("id")
    transformers = Transformer.objects.all()
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["path","type","voltage","room","description"])
        for panel in panels:
            for transformer in transformers:
                if str(transformer.FQN + ".") in panel.FQN:
                    writer.writerow([transformer.FQN, "Transformer", "277/480", "", ""])
                    writer.writerow(["","","","",""])
                    transformers=transformers.exclude(Name=transformer.Name)
                    break
            try:
                writer.writerow([panel.FQN, "Panel", panel.Voltage, panel.Closet.Old_Name, panel.Notes])
                for circuit in panel.circuits().order_by("id"):
                    writer.writerow([circuit.FQN, "Circuit", panel.Voltage, panel.Closet.Old_Name, circuit.Notes])
            except:
                writer.writerow([panel.FQN, "Panel", panel.Voltage, "", panel.Notes])
                for circuit in panel.circuits().order_by("id"):
                    writer.writerow([circuit.FQN, "Circuit", panel.Voltage, "", circuit.Notes])
            writer.writerow(["", "", "", "", ""])
    file_name = file_name.replace("panels", "devices")
    devices = Device.objects.filter(School = school).order_by('id')
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["DeviceObj","Circuit","Location","Description","Three Phase"])
        for device in devices:
            try:
                for circuit in device.Circuit.all().order_by("id"):
                    if device.Circuit.all().count() > 1:
                        writer.writerow([device.Name, circuit.FQN, device.Room.OldName, device.Notes, "X"])
                    else:
                        writer.writerow([device.Name, circuit.FQN, device.Room.OldName, device.Notes, ""])
            except Exception as e:
                #print(e)
                try:
                    for circuit in device.Circuit.all().order_by("id"):
                        if device.Circuit.all().count() > 1:
                            writer.writerow([device.Name, circuit.FQN, "", device.Notes, "X"])
                        else:
                            writer.writerow([device.Name, circuit.FQN, "", device.Notes, ""])
                except:
                    writer.writerow([device.Name,"", device.Room.OldName, device.Notes, ""])
    file_name = file_name.replace("devices", "device_relations")
    with open(file_name, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["Device","Associated Device","Power","Zone"])
        for device in devices:
            if not device.Associated_Device == None:
                writer.writerow([device.Name, device.Associated_Device.Name, device.Power, device.Location])
            else:
                writer.writerow([device.Name, "", device.Power, device.Location])

