from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *
import codecs


def panel_editing(request, panel_id):
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    form = PanelEditForm(initial={'Name': panel_obj.Name})
    if request.POST.get("Save Name"):
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
        panel_obj.Voltage = request.POST.get("Voltage")
        panel_obj.save()
    if request.POST.get("Save Notes"):
        panel_obj.Notes = request.POST.get("Notes")
        panel_obj.save()
    if request.POST.get("Save Parent"):
        panel_obj.Parent = Panel.objects.get(id=request.POST.get("Parent"))
        panel_obj.save()
    if request.POST.get("Save Closet"):
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
        f = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "r")
        file = str(f.read())
        w = codecs.open("/var/www/gismap/energize_andover/templates/energize_andover/ChangeLog.html", "w")
        w.write(file[0:file.index("</p>") + 4] + "\n<p>School: " + room_obj.School.Name + " User: " + request.session['username'] + " Description: Room Name Changed: " + room_obj.Name + "-->" + request.POST.get("Name") + "</p>" + file[file.index("</p>") + 4:])
        room_obj.Name = request.POST.get("Name")
        room_obj.save()

    if request.POST.get("Save Old Name"):
        room_obj.OldName = request.POST.get("Old Name")
        room_obj.save()
    if request.POST.get("Save Type"):
        room_obj.Type = request.POST.get("Type")
        room_obj.save()
    if request.POST.get("Save Notes"):
        room_obj.Notes = request.POST.get("Notes")
        room_obj.save()
    if request.POST.get("Add Panel"):
        print (request.POST.get("Panels"))
        pan = Panel.objects.get(pk=request.POST.get("Panels"))
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

    form = PanelEditForm(initial={'Name': room_obj.Name})
    return HttpResponse(render(request, "energize_andover/Room.html", {'room': room_obj,
                                                                       'form': form,
                                                                       'Panels': Panel.objects.all(),
                                                                       'room_panels': room_obj.Panels.all()}))

def device_editing(request, device_id):
    None

def circuit_editing (request, circuit_id):
    None