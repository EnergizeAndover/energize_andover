from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404

from .models import *
import pandas as pd
import requests
from django.conf.urls import url
#from forms import MetasysUploadForm, GraphUploadForm, SmartGraphUploadForm

from energize_andover.forms import *
from energize_andover.script.file_transfer import get_transformed_file, graph_transformed_file, _temporary_output_file_path
from energize_andover.script.file_transfer_grapher import get_transformed_graph
#from energize_andover.script.electrical_mapping_parse import create_mapping
from energize_andover.script.circuit_room_relationships import parse
from django.core.urlresolvers import reverse

def index(request):
    # Handle file upload
    if request.method == 'POST' and request.POST.get('parse'):
        print(request.POST)
        form = MetasysUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)

        if form.is_valid():

            data = form.cleaned_data
            if not data['graph']:

                return get_transformed_file(data)
            else:
                get_transformed_file(data)
                form2 = SmartGraphUploadForm()
                return HttpResponse(render(request, 'energize_andover/index.html',
                                           context={'title': 'Metasys Parsing',
                                                    'form2': form2}))
    elif request.method == 'POST' and request.POST.get('graph'):
        form2 = SmartGraphUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)
        if form2.is_valid():
            return graph_transformed_file(form2.cleaned_data)
        else:
            return HttpResponse(render(request, 'energize_andover/index.html',
                                       context={'title': 'Metasys Parsing',
                                                'form2': form2}))
    else:
        form = MetasysUploadForm()  # An empty, unbound form

    # Render list page with the documents and the form
    return HttpResponse(render(request, 'energize_andover/index.html',
                               context={'title': 'Metasys Parsing', 'form': form}))


def grapher(request):
    #Handle file upload
    if request.method == 'POST':
        form = GraphUploadForm(request.POST, request.FILES)
        print('post is %s' % request.POST)
        if form.is_valid():
            return render(get_transformed_graph(form.cleaned_data))
    else:
        form = GraphUploadForm()

    # Render list page with the documents and the form
    return HttpResponse(render(request, 'energize_andover/grapher.html',
                               context={'title': 'Grapher', 'form': form}))

def electrical_mapping(request):
    if request.method == 'POST':
        if request.POST.get('Start'):
            form = NewSchoolForm()
            return render(request, 'energize_andover/Electrical.html',
                  {'title': 'Add School', 'form': form})
        else:
            form = NewSchoolForm(request.POST, request.FILES)
            if form.is_valid():
                data = form.cleaned_data
                newSchool = School(Name=data['Name'])
                newSchool.save()
            else:
                error ='invalid form'
                return render(request, 'energize_andover/Electrical.html',
                              {'form': form, 'error': error})
    schools = School.objects.filter()
    return render(request, 'energize_andover/Electrical.html',
                  {'title': 'School Select', 'schools': schools})

def school(request, school_id):
    school_obj = get_object_or_404(School,
                                   pk=school_id)
    print(school_obj)
    Closets = school_obj.closets()
    Panels = school_obj.panels()
    Rooms = school_obj.rooms()
    form = SearchForm()
    devices = Circuit.objects.all()
    for i in range (0, len(Panels)):
        if Panels[i] in devices:
            devices.remove(Panels[i])

    fdevices = []
    for i in range(0, len(devices)):
        if devices[i].Function != "NA":
            fdevices.append(devices[i])
    return render(request, 'energize_andover/School.html',
                  {'title': 'School Select', 'school': school_obj,
                   'Rooms': Rooms, 'Panels': Panels, 'Closets': Closets, 'Devices': fdevices,
                   'form': form})


def panel(request, panel_id):
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    if panel_obj.rooms() is not None:
        Rooms = panel_obj.rooms()
    if panel_obj.circuits() is not None:
        Circuits = panel_obj.circuits()
    if panel_obj.panels() is not None:
        Panels = panel_obj.panels()
    parray = []
    for i in range(0, len(Circuits)):
        parray.append(Circuits[i])
    #print (parray[len(parray) - 1])
    print (parray)
    name = ""
    rarray = []
    for i in range(0, len(Panels)):
        panel = Panels[i]
        name = panel.FQN[0: panel.FQN.index(panel.Name) - 1]
        for j in range (0, len(parray)):
            print (parray[j])
            if parray[j].FQN == name and parray[j] not in rarray:
                rarray.append(parray[j])
    for i in range(0, len(rarray)):
        print (rarray[i])
        parray.remove(rarray[i])
    #print (parray)
    if panel_obj.School is not None:
        school = panel_obj.School
    Main = Panel.objects.filter(Name='MSWB')
    if Main.count()>0:
        Main = Main[0]

    picture = "energize_andover/" + panel_obj.Name.replace(" ", "") + ".jpg"
    print (picture)
    return render(request, 'energize_andover/Panel.html',
                  {'panel' : panel_obj,
                   'Rooms': Rooms, 'Circuits': parray,
                   'Subpanels' : Panels, 'Main' : Main, 'school': school,
                   'picture' : picture})

def room(request, room_id):
    room_obj = get_object_or_404(Room, pk=room_id)
    School = room_obj.school()
    Panels = room_obj.panels()
    Circuits = room_obj.circuits()
    #Circuits = Circuit.objects.filter(Rooms = room_obj)
    return render (request, 'energize_andover/Room.html',
                   {'room' : room_obj,
                    "school": School,
                    'Panels': Panels,
                    'Circuits': Circuits})

def circuit(request, circuit_id):
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    Rooms = circuit_obj.rooms()
    school = circuit_obj.Panel.School
    return render(request, 'energize_andover/Circuit.html',
                  {'circuit': circuit_obj, 'Rooms': Rooms, 'school' : school})

def closet(request, closet_id):
    closet_obj = get_object_or_404(Closet, pk=closet_id)
    panels = Panel.objects.filter(Closet__pk=closet_id)
    return render(request, 'energize_andover/Closet.html',
                  {'closet': closet_obj, 'panels': panels})

def adder(request):
    if request.method == 'POST':
        if request.POST.get('start'):
            print(request.POST)
            form = AdderTypeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['type'] == 'school':
                    form = SchoolForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'school': form, 'title': 'Electrical Mapping Creation'})
                elif data['type'] == 'closet':
                    form = ClosetForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'closet': form, 'title': 'Electrical Mapping Creation'})
                elif data['type'] == 'panel':
                    form = PanelForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'panel': form, 'title': 'Electrical Mapping Creation'})
                elif data['type'] == 'room':
                    form = RoomForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'room': form, 'title': 'Electrical Mapping Creation'})
                elif data['type'] == 'circuit':
                    form = CircuitForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'circuit': form, 'title': 'Electrical Mapping Creation'})
        elif request.POST.get('school'):
            form = SchoolForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.save()
                form = AdderTypeForm()
                return render(request, 'energize_andover/Adder.html',
                              {'type': form, 'title': 'Electrical Mapping Creation',
                               'complete': 'school'})
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'school': form, 'title': 'Electrical Mapping Creation'})
        elif request.POST.get('closet'):
            form = ClosetForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.save()
                form = AdderTypeForm()
                return render(request, 'energize_andover/Adder.html',
                              {'type': form, 'title': 'Electrical Mapping Creation',
                               'complete': 'school'})
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'closet': form, 'title': 'Electrical Mapping Creation'})
        elif request.POST.get('panel'):
            form = PanelForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.save()
                form = AdderTypeForm()
                return render(request, 'energize_andover/Adder.html',
                              {'type': form, 'title': 'Electrical Mapping Creation',
                               'complete': 'school'})
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'panel': form, 'title': 'Electrical Mapping Creation'})
        elif request.POST.get('room'):
            form = RoomForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.save()
                form = AdderTypeForm()
                return render(request, 'energize_andover/Adder.html',
                              {'type': form, 'title': 'Electrical Mapping Creation',
                               'complete': 'school'})
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'room': form, 'title': 'Electrical Mapping Creation'})
        elif request.POST.get('circuit'):
            form = CircuitForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.save()
                form = AdderTypeForm()
                return render(request, 'energize_andover/Adder.html',
                              {'type': form, 'title': 'Electrical Mapping Creation',
                               'complete': 'school'})
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'circuit': form, 'title': 'Electrical Mapping Creation'})
    else:
        form = AdderTypeForm()
    return render(request, 'energize_andover/Adder.html',
                  {'type': form, 'title': 'Electrical Mapping Creation'})


def populate(request):


    if request.method == 'POST':
        form = PopulationForm(request.POST, request.FILES)
        if form.is_valid():
            parse(form.cleaned_data)
            return render(request, 'energize_andover/Population.html',)
    else:
        form = PopulationForm()
    return render(request, 'energize_andover/Population.html',
                  {'form':form})

def search(request):
    if request.method == 'GET':
        form = SearchForm(request.GET, request.FILES)
        if form.is_valid():
            title = ""
            title = request.GET.get('entry')

            panels = []
            circuits = []
            rooms = []
            closets = []

            if request.GET.get('panels') == 'on':
                #panels = Panel.objects.filter(Name = title)
                all_panels = Panel.objects.all()
                for i in range (0, len(all_panels)):
                    try:
                        if title.lower() == all_panels[i].Name[0:len(title)].lower():
                            #print(all_panels[i])
                            panels.append(all_panels[i])
                    except:
                        None
            if request.GET.get('circuits') == 'on':
                all_circuits = Circuit.objects.all()
                for i in range(0, len(all_circuits)):
                    try:
                        if title.lower() == all_circuits[i].Name[0:len(title)].lower():
                            # print(all_panels[i])
                            circuits.append(all_circuits[i])
                    except:
                        None
                    try:
                        if title.lower() in all_circuits[i].Function[0:len(title)].lower():
                            circuits.append(all_circuits[i])
                    except:
                        None
            if request.GET.get('rooms') == 'on':
                all_rooms = Room.objects.all()
                for i in range(0, len(all_rooms)):
                    try:
                        if title.lower() == all_rooms[i].Name.lower():
                            # print(all_panels[i])
                            rooms.append(all_rooms[i])
                    except:
                        None
                    try:
                        if title.lower() == all_rooms[i].OldName.lower():
                            rooms.append(all_rooms[i])
                    except:
                        None
                    try:
                        if title.lower() in all_rooms[i].Type.lower():
                            rooms.append(all_rooms[i])
                    except:
                        None
            if request.GET.get('closets') == 'on':
                all_closets = Closet.objects.all()
                for i in range(0, len(all_closets)):
                    try:
                        if title.lower() == all_closets[i].Name.lower():
                            # print(all_panels[i])
                            closets.append(all_closets[i])
                    except:
                        None
                    try:
                        if title.lower() == all_closets[i].Old_Name.lower():
                            closets.append(all_closets[i])
                    except:
                        None
            return render(request, 'energize_andover/Search.html', {'form': form, 'title': title,
                            'panels': panels, 'circuits': circuits, 'rooms': rooms, 'closets': closets})
        return render(request, 'energize_andover/Search.html', {'form': form, 'title': ""})
    else:
        form = SearchForm()
    return HttpResponse(render(request, 'energize_andover/Search.html', context = {'form': form, 'title': ""}))

def dictionary (request):
    return render(request, 'energize_andover/Dictionary.html')