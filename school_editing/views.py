from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *

def panel_editing(request, panel_id):
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    form = PanelEditForm(initial={'Name': panel_obj.Name,
                                  'Voltage': panel_obj.Voltage,
                                  'Notes': panel_obj.Notes})
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
    form = PanelEditForm(request.POST)
    return HttpResponse(request, "energize_andover/Room.html", {'room': room_obj, 'form': form})

def device_editing(request, device_id):
    None

def circuit_editing (request, circuit_id):
    None