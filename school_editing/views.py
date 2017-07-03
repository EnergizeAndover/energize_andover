from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *
import codecs
from datetime import datetime
from login.views import check_status, check_school_privilege


def panel_editing(request, panel_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    if check_school_privilege(panel_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    form = PanelEditForm(initial={'Name': panel_obj.Name})
    if request.POST.get("Save Name"):
        message = "Panel Name Change: " + panel_obj.Name + " -->" + request.POST.get(
            "Name") + ". All Affected Circuits and Panels renamed accordingly. "
        update_log(message, panel_obj.School, request)
        name = panel_obj.Name
        panel_obj.Name = request.POST.get("Name")
        panel_obj.save()
        panels = Panel.objects.all()
        for pan in panels:
            if name in pan.FQN:
                pan.FQN = pan.FQN.replace(name, request.POST.get("Name"))
                pan.save()
        circuits = Circuit.objects.all()
        for circ in circuits:
            if name in circ.FQN:
                circ.FQN = circ.FQN.replace(name, request.POST.get("Name"))
                circ.save()
            if name in circ.Name:
                circ.Name = circ.Name.replace(name, request.POST.get("Name"))
                circ.save()

    if request.POST.get("Save Voltage"):
        message = "Panel Voltage Change: " + panel_obj.Voltage + " -->" + request.POST.get("Voltage")
        update_log(message, panel_obj.School, request)
        panel_obj.Voltage = request.POST.get("Voltage")
        panel_obj.save()
    if request.POST.get("Save Notes"):
        message = "Panel Notes Change: " + panel_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, panel_obj.School, request)
        panel_obj.Notes = request.POST.get("Notes")
        panel_obj.save()
    if request.POST.get("Save Parent"):
        par_pan = panel_obj.Panels.Name
        new_par_pan = Panel.objects.get(id=request.POST.get("Panels")).Name
        message = "Parent Panel Change on " + panel_obj.Name + ": " + par_pan + " -->" + new_par_pan + ". All Affected Circuits and Panels renamed accordingly. "
        update_log(message, panel_obj.School, request)
        panel_obj.Panels = Panel.objects.get(id=request.POST.get("Panels"))
        panel_obj.save()
        panels = Panel.objects.all()
        for pan in panels:
            if par_pan in pan.FQN and panel_obj.Name in pan.FQN:
                pan.FQN = pan.FQN.replace(par_pan, new_par_pan)
                pan.save()
        circuits = Circuit.objects.all()
        for circ in circuits:
            if par_pan in circ.FQN and panel_obj.Name in circ.FQN:
                circ.FQN = circ.FQN.replace(par_pan, new_par_pan)
                circ.save()
    if request.POST.get("Save Closet"):
        message = "Panel Closet Change: " + panel_obj.Closet + " -->" + request.POST.get("Closet")
        update_log(message, panel_obj.School, request)
        panel_obj.Closet = Closet.objects.get(id=request.POST.get("Closet"))
        panel_obj.save()
    return HttpResponse(render(request, 'energize_andover/Panel.html',
                  {'panel': panel_obj,
                   'form': form,
                   'Panels': Panel.objects.all(),
                   'Closets': Closet.objects.all()}))

def room_editing (request, room_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    room_obj = get_object_or_404(Room, pk=room_id)
    if check_school_privilege(room_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    if request.POST.get("Save Name"):
        message = "Room Number Change: " + room_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, room_obj.School, request)
        room_obj.Name = request.POST.get("Name")
        room_obj.save()
    if request.POST.get("Save Old Name"):
        message = "Old Room Number Change: " + room_obj.OldName + " -->" + request.POST.get("Old Name")
        update_log(message, room_obj.School, request)
        room_obj.OldName = request.POST.get("Old Name")
        room_obj.save()
    if request.POST.get("Save Type"):
        message = "Room Type Change: " + room_obj.Type + " -->" + request.POST.get("Type")
        update_log(message, room_obj.School, request)
        room_obj.Type = request.POST.get("Type")
        room_obj.save()
    if request.POST.get("Save Notes"):
        message = "Room Notes Change: " + room_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, room_obj.School, request)
        room_obj.Notes = request.POST.get("Notes")
        room_obj.save()
    """
    if request.POST.get("Add Panel"):

        pan = Panel.objects.get(pk=request.POST.get("Panels"))
        message = "Panel " + pan.Name + " added to Room " + room_obj.Name
        update_log(message, room_obj.School, request)
        room_obj.Panels.add(pan)
        room_obj.save()
    for panel in room_obj.Panels.all():
        if request.POST.get(panel.Name):
            room_obj.Panels.remove(panel)
            room_obj.save()
            for circuit in Circuit.objects.filter(Panel=panel):
                if room_obj in circuit.Rooms.all():
                    circuit.Rooms.remove(room_obj)
                    circuit.save()
                for device in Device.objects.filter(Circuit = circuit):
                    if room_obj in device.Room:
                        device.Room.remove(room_obj)
                        device.save()
            message = "Panel " + panel + " removed from Room " + room_obj.Name + \
                ". All Circuits and Devices on this panel that are related to this room are no longer related."
            update_log(message, room_obj.School, request)
    """
    form = PanelEditForm(initial={'Name': room_obj.Name})
    return HttpResponse(render(request, "energize_andover/Room.html", {'room': room_obj,
                                                                       'form': form,
                                                                       'Panels': Panel.objects.all(),
                                                                       'room_panels': room_obj.Panels.all()}))

def device_editing(request, device_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    device_obj = get_object_or_404(Device, pk = device_id)
    if check_school_privilege(device_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    form = PanelEditForm(initial={'Name': device_obj.Name})
    if request.POST.get("Save Name"):
        message = "Device Name Change: " + device_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, device_obj.School, request)
        device_obj.Name = request.POST.get("Name")
        device_obj.save()
    if request.POST.get("Save Power"):
        message = "Device Power Change: " + device_obj.Power + " -->" + request.POST.get("Power")
        update_log(message, device_obj.School, request)
        device_obj.Power = request.POST.get("Power")
        device_obj.save()
    if request.POST.get("Save Zone"):
        message = "Device Zone Change: " + device_obj.Location + " -->" + request.POST.get("Zone")
        update_log(message, device_obj.School, request)
        device_obj.Location = request.POST.get("Zone")
        device_obj.save()
    if request.POST.get("Save Notes"):
        message = "Device Notes Change: " + device_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, device_obj.School, request)
        device_obj.Notes = request.POST.get("Notes")
        device_obj.save()
    query = "Enter Query (Name of Device)     |"
    devices = []
    if request.POST.get("Search"):
        query = request.POST.get("Associated_Device_Query")
        devs = Device.objects.all()
        for dev in devs:
            if query == dev.Name:
                devices.insert(0, dev)
            elif query in dev.Name:
                devices.append(dev)
    if request.POST.get("Save Associated Device"):
        dev_id = request.POST.get("Associated_Dev")
        assoc_dev = Device.objects.get(id= dev_id)
        message = device_obj.to_string() + " is now associated with " + assoc_dev.to_string() +"."
        update_log(message, device_obj.School, request)
        device_obj.Associated_Device = assoc_dev
        device_obj.save()
        assoc_dev.Associated_Device = device_obj
        assoc_dev.save()

    return HttpResponse(render(request, "energize_andover/Device.html", {'device': device_obj,
                                                                        'devices': devices,
                                                                         'query':query,
                                                                         'form': form}))

def circuit_editing (request, circuit_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    if check_school_privilege(circuit_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    if request.POST.get("Save Name"):
        message = "Circuit Name Change: " + circuit_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, circuit_obj.School, request)
        circuit_obj.Name = request.POST.get("Name")
        circuit_obj.save()
    if request.POST.get("Save Number"):
        message = "Circuit Number Change: " + circuit_obj.Number + " -->" + request.POST.get("Number")
        update_log(message, circuit_obj.School, request)
        circuit_obj.Number = request.POST.get("Number")
        circuit_obj.save()
    if request.POST.get("Save Notes"):
        message = "Circuit Notes Change: " + circuit_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, circuit_obj.School, request)
        circuit_obj.Notes = request.POST.get("Notes")
        circuit_obj.save()
    query = "Enter Query (Name of Device)     |"
    devices = []
    for dev in circuit_obj.devices():
        if request.POST.get(dev.Name):
            message = "Circuit-Device Change: Device " + dev.Name + " removed from Circuit " + circuit_obj.Name
            update_log(message, circuit_obj.School, request)
            dev.Circuit.remove(circuit_obj)
            try:
                remove = True
                for device in circuit_obj.devices():
                    if dev.Room == device.Room:
                        remove = False
                if remove:
                    circuit_obj.Rooms.remove(dev.Room)
                    circuit_obj.save()
                panel = circuit_obj.Panel
                remove = True
                room = dev.Room
                for circuit in panel.circuits():
                    if not circuit == circuit_obj:
                        for device in circuit.devices():
                            try:
                                if device.Room == room:
                                    print (circuit)
                                    remove = False
                            except:
                                None
                if remove:
                    room.Panels.remove(panel)
                    room.save()
            except:
                None
            #dev.save()
    if request.POST.get("Search"):
        query = request.POST.get("Device_Query")
        devs = Device.objects.all()
        for dev in devs:
            if query == dev.to_string():
                devices.insert(0, dev)
            elif query in dev.to_string():
                devices.append(dev)
    if request.POST.get("Add Device"):
        dev_id = request.POST.get("Device")
        added_dev = Device.objects.get(id= dev_id)
        message = "Device " + added_dev.to_string() + " added to Circuit " + circuit_obj.Name +"."
        update_log(message, circuit_obj.School, request)
        added_dev.Circuit.add(circuit_obj)
        added_dev.save()
        try:
            circuit_obj.Rooms.add(added_dev.Room)
            circuit_obj.save()
            panel = circuit_obj.Panel
            room = added_dev.Room
            room.Panels.add(panel)
            room.save()
        except:
            None

    form = PanelEditForm(initial={'Name': circuit_obj.Name})
    return HttpResponse(render(request, "energize_andover/Circuit.html", {'circuit': circuit_obj,
                                                                          'devices': circuit_obj.devices(),
                                                                          'search_devices': devices,
                                                                          'query':query,
                                                                         'form': form}))

def closet_editing(request, closet_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    closet_obj = get_object_or_404(Circuit, pk=closet_id)
    if check_school_privilege(closet_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    form = PanelEditForm(initial={'Name': closet_obj.Name})
    return HttpResponse(render(request, "energize_andover/Closet.html", {'closet': closet_obj,
                                                                          'form': form}))
def update_log (message, school, request):
    f = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "r")
    file = str(f.read())
    w = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "w")
    break_pt = file.index("</h1>") + 5
    w.write(file[0:break_pt] + "\n<p>Time: " + str(datetime.now()) + ", School: " + school.Name + ", User: " + request.session[
        'username'] + ", Description: " + message + "</p>" + file[break_pt:])