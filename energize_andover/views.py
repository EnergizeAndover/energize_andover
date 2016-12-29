from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from .models import *
import pandas as pd
import requests
from django.conf.urls import url
#from forms import MetasysUploadForm, GraphUploadForm, SmartGraphUploadForm

from energize_andover.forms import *
from energize_andover.script.file_transfer import get_transformed_file, graph_transformed_file, _temporary_output_file_path
from energize_andover.script.file_transfer_grapher import get_transformed_graph
from energize_andover.script.electrical_mapping_parse import create_mapping

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
    Closets = school_obj.closets()
    Panels = school_obj.panels()
    Rooms = school_obj.rooms()
    return render(request, 'energize_andover/School.html',
                  {'title': 'School Select', 'school': school_obj,
                   'Rooms': Rooms, 'Panels': Panels, 'Closets': Closets})


def panel(request, panel_id):
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    if panel_obj.rooms() is not None:
        Rooms = panel_obj.rooms()
    if panel_obj.circuits() is not None:
        Circuits = panel_obj.circuits()
    if panel_obj.panels() is not None:
        Panels = panel_obj.panels()
    if panel_obj.School is not None:
        school = panel_obj.School
    Main = Panel.objects.filter(Name='MSWB')
    if Main.count()>0:
        Main = Main[0]
    return render(request, 'energize_andover/Panel.html',
                  {'panel' : panel_obj, 'Rooms': Rooms, 'Circuits': Circuits,
                   'Subpanels' : Panels, 'Main' : Main, 'school': school})

def room(request, room_id):
    room_obj = get_object_or_404(Room, pk=room_id)
    Panels =  room_obj.panels()
    #School = room_obj.school()
    Circuits = room_obj.circuits()
    return render (request, 'energize_andover/Room.html',
                   {'room' : room_obj, 'Panels': Panels,
                    #'School': School,
                    'Circuits': Circuits})

def circuit(request, circuit_id):
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    Rooms = circuit_obj.rooms()
    return render(request, 'energize_andover/Circuit.html',
                  {'circuit': circuit_obj, 'Rooms': Rooms})

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
            create_mapping(form.cleaned_data)
            return render(request, 'energize_andover/Population.html',)
    else:
        form = PopulationForm()
    return render(request, 'energize_andover/Population.html',
                  {'form':form})
