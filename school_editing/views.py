from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *
import codecs
from datetime import datetime


def panel_editing(request, panel_id):
    panel_obj = get_object_or_404(Panel, pk=panel_id)
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
    room_obj = get_object_or_404(Room, pk=room_id)
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
                if room_obj in circuit.Rooms:
                    circuit.Rooms.remove(room_obj)
                    circuit.save()
                for device in Device.objects.filter(Circuit = circuit):
                    if room_obj in device.Room:
                        device.Room.remove(room_obj)
                        device.save()
            message = "Panel " + panel + " added to Room " + room_obj.Name + \
                ". All Circuits and Devices on this panel that are related to this room are no longer related."
            update_log(message, room_obj.School, request)

    form = PanelEditForm(initial={'Name': room_obj.Name})
    return HttpResponse(render(request, "energize_andover/Room.html", {'room': room_obj,
                                                                       'form': form,
                                                                       'Panels': Panel.objects.all(),
                                                                       'room_panels': room_obj.Panels.all()}))

def device_editing(request, device_id):
    device_obj = get_object_or_404(Device, pk = device_id)
    form = PanelEditForm(initial={'Name': device_obj.Name})
    return HttpResponse(render(request, "energize_andover/Room.html", {'device': device_obj,
                                                                       'form': form}))

def circuit_editing (request, circuit_id):
    None

def update_log (message, school, request):
    f = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "r")
    file = str(f.read())
    w = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "w")
    break_pt = file.index("</h1>") + 5
    w.write(file[0:break_pt] + "\n<p>Time: " + str(datetime.now()) + ", School: " + school.Name + ", User: " + request.session[
        'username'] + ", Description: " + message + "</p>" + file[break_pt:])