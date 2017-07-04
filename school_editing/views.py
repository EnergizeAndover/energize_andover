from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *
from energize_andover.forms import *
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
    par_circuits = panel_obj.Panels.circuits()
    selected_panel = None
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
        par_circuits = Panel.objects.get(id=request.POST.get("Panels")).circuits()
        selected_panel = Panel.objects.filter(id=request.POST.get("Panels"))
    if request.POST.get("Save Circuit"):
        new_par_pan = Panel.objects.get(id=request.POST.get("Panels")).Name
        circ = Circuit.objects.get(id=request.POST.get("Circuit"))
        try:
            par_pan = panel_obj.Panels.Name
            message = "Parent Panel Change on " + panel_obj.Name + ": " + par_pan  + " -->" + new_par_pan + ". All Affected Circuits and Panels renamed accordingly. "
        except:
            message = "Parent Panel for " + panel_obj.Name + " set to " + new_par_pan
        update_log(message, panel_obj.School, request)
        panel_obj.Panels = Panel.objects.get(id=request.POST.get("Panels"))
        #panel_obj.FQN = new_par_pan + str(circ.Number) + panel_obj.Name
        panel_obj.save()
        for circuit in Circuit.objects.all():
            if panel_obj.Name in circuit.FQN:
                circuit.FQN = new_par_pan + str(circ.Number) + circuit.Name
                circuit.save()
        for panel in Panel.objects.all():
            if panel_obj.Name in panel.FQN:
                breakpt = panel.FQN.index(panel_obj.Name)
                remainder = panel.FQN[breakpt:]
                panel.FQN = new_par_pan + str(circ.Number) + remainder
                panel.save()

    if request.POST.get("Save Closet"):
        message = "Panel Closet Change: " + panel_obj.Closet + " -->" + request.POST.get("Closet")
        update_log(message, panel_obj.School, request)
        panel_obj.Closet = Closet.objects.get(id=request.POST.get("Closet"))
        panel_obj.save()
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Panel " + panel_obj.Name + " Deleted. All Circuits also Deleted"
            update_log(message, panel_obj.School, request)
            for circuit in panel_obj.circuits():
                circuit.delete()
            school_obj = panel_obj.School
            panels = panel_obj.panels()
            for pan in panels:
                print(pan.Name)
                pan.Panels = None
                print (pan.Panels)
                pan.save()
            panel_obj.delete()
            return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))

    return HttpResponse(render(request, 'energize_andover/Panel.html',
                  {'panel': panel_obj,
                   'form': form,
                   'Panels': Panel.objects.all(),
                   'selected': selected_panel,
                   'par_circuits': par_circuits,
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
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Room " + room_obj.Name + " Deleted."
            update_log(message, room_obj.School, request)
            school_obj = room_obj.School
            for device in Device.objects.filter(Room = room_obj):
                device.Room = None
                device.save()
            room_obj.delete()
            return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))
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
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Device " + device_obj.to_string() + " Deleted."
            update_log(message, device_obj.School, request)
            school_obj = device_obj.School
            device_obj.delete()
            return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))
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
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Circuit " + circuit_obj.Name + " Deleted."
            update_log(message, circuit_obj.School, request)
            school_obj = circuit_obj.School
            #print(Device.objects.filter(Circuit=circuit_obj))
            for device in Device.objects.filter(Circuit=circuit_obj):
                print(device.Circuit.all())
                device.Circuit.remove(circuit_obj)
                device.save()
                print(device.Circuit.all())
            circuit_obj.delete()
            return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))
    form = PanelEditForm(initial={'Name': circuit_obj.Name})
    return HttpResponse(render(request, "energize_andover/Circuit.html", {'circuit': circuit_obj,
                                                                          'devices': circuit_obj.devices(),
                                                                          'search_devices': devices,
                                                                          'query':query,
                                                                         'form': form}))

def closet_editing(request, closet_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    closet_obj = get_object_or_404(Closet, pk=closet_id)
    if check_school_privilege(closet_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")

    if request.POST.get("Save Name"):
        message = "Closet Number Change: " + closet_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, closet_obj.School, request)
        closet_obj.Name = request.POST.get("Name")
        closet_obj.save()
    if request.POST.get("Save Old Name"):
        message = "Old Closet Number Change: " + closet_obj.Old_Name + " -->" + request.POST.get("Old Name")
        update_log(message, closet_obj.School, request)
        closet_obj.Old_Name = request.POST.get("Old Name")
        closet_obj.save()
    if request.POST.get("Save Notes"):
        message = "Closet Notes Change: " + closet_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, closet_obj.School, request)
        closet_obj.Notes = request.POST.get("Notes")
        closet_obj.save()
    if request.POST.get("Add Panel"):
        pan = Panel.objects.get(pk=request.POST.get("Panels"))
        try:
            message = "Panel " + pan.Name + " moved from Closet " + pan.Closet.Name + " to Closet " +  closet_obj.Name
        except:
            message = "Panel " + pan.Name + " moved to Closet " +  closet_obj.Name
        update_log(message, closet_obj.School, request)
        pan.Closet = closet_obj
        pan.save()
    for panel in Panel.objects.filter(Closet = closet_obj):
        if request.POST.get(panel.Name):
            panel.Closet = None
            panel.save()
            message = "Panel " + panel.Name + " removed from Closet " + closet_obj.Name
            update_log(message, closet_obj.School, request)
    form = PanelEditForm(initial={'Name': closet_obj.Name})
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Closet " + closet_obj.Name + " Deleted."
            update_log(message, closet_obj.School, request)
            school_obj = closet_obj.School
            for panel in Panel.objects.filter(Closet=closet_obj):
                panel.Closet = None
                panel.save()
            closet_obj.delete()
            return HttpResponseRedirect("/energize_andover/School"+str(school_obj.pk))

    return HttpResponse(render(request, "energize_andover/Closet.html", {'closet': closet_obj,
                                                                         'clos_panels': Panel.objects.filter(Closet = closet_obj),
                                                                         'Panels': Panel.objects.all(),
                                                                          'form': form}))
def update_log (message, school, request):
    f = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "r")
    file = str(f.read())
    w = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "w")
    break_pt = file.index("</h1>") + 5
    w.write(file[0:break_pt] + "\n<p>Time: " + str(datetime.now()) + ", School: " + school.Name + ", User: " + request.session[
        'username'] + ", Description: " + message + "</p>" + file[break_pt:])