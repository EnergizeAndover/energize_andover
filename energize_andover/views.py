from django.http import HttpResponse, Http404, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from django.contrib.sessions.models import Session
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
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index ("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
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
    if (request.GET.get('mybtn')):
        request.session['logged_in'] = None
        return HttpResponseRedirect("Login")
    schools = School.objects.filter()
    return render(request, 'energize_andover/Electrical.html',
                  {'title': 'School Select', 'schools': schools})

def school(request, school_id):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
    school_obj = get_object_or_404(School,
                                   pk=school_id)
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if school_obj not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    Closets = school_obj.closets()
    Panels = school_obj.panels()
    Rooms = school_obj.rooms()
    form = SearchForm()
    devices = school_obj.devices()
    if len(devices) == 0:
        devices = Panel.objects.filter(Name = "THIS IS A PLACEHOLDER. THIS IS INTENDED TO RETURN AN EMPTY QUERYSET. OTHERWISE THE PROGRAM IS LESS AESTHETICALLY PLEASING.")

    return render(request, 'energize_andover/School.html',
                  {'title': 'School Select', 'school': school_obj,
                   'Rooms': Rooms, 'Panels': Panels, 'Closets': Closets, 'Devices': devices,
                   'form': form})

def device(request, device_id):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
    user = authenticate(username=request.session['username'], password=request.session['password'])
    device_ = get_object_or_404(Device, pk=device_id)
    rooms = device_.rooms()
    circuits = device_.circuits()
    circ = circuits.first()
    print (circ)
    panel_ = circ.Panel
    school_ = panel_.School
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if school_ not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    assoc_dev = device_.Associated_Device
    #print(assoc_dev.to_string)
    return render(request, 'energize_andover/Device.html',
                  {'device': device_, "room": rooms, 'school': school_, 'circuit': circuits, 'assoc_device': assoc_dev})

def panel(request, panel_id):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if panel_obj.School not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    if panel_obj.rooms() is not None:
        Rooms = panel_obj.rooms()
    if panel_obj.circuits() is not None:
        Circuits = panel_obj.circuits()
    if panel_obj.panels() is not None:
        Panels = panel_obj.panels()
    parray = []
    for i in range(0, len(Circuits)):
        parray.append(Circuits[i])
    name = ""
    rarray = []
    transformers = Transformer.objects.all()
    for i in range(0, len(Panels)):
        a_break = False
        panel = Panels[i]
        path = panel.FQN
        #print (path)
        for count in reversed(range(6)):
            for j in range(0, len(transformers)):
                if len(transformers[j].Name) == count:
                    print (count)
                    if transformers[j].Name in path:
                        print (transformers[j].Name)
                        print(path)
                        path = path.replace(transformers[j].Name, "")

        print (path)
        name = path[0: path.index(panel.Name) - 1]
        print(name)
        for j in range (0, len(parray)):
            print (parray[j].FQN)
            if parray[j].FQN == name and parray[j] not in rarray:
                rarray.append(parray[j])
    for i in range(0, len(rarray)):
        print (rarray[i])
        parray.remove(rarray[i])

    print (parray)
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
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
    room_obj = get_object_or_404(Room, pk=room_id)
    School = room_obj.school()
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if School not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    Panels = room_obj.panels()
    Circuits = room_obj.circuits()
    #Circuits = Circuit.objects.filter(Rooms = room_obj)
    return render (request, 'energize_andover/Room.html',
                   {'room' : room_obj,
                    "school": School,
                    'Panels': Panels,
                    'Circuits': Circuits})

def circuit(request, circuit_id):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    Rooms = circuit_obj.rooms()
    school = circuit_obj.Panel.School
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if school not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    devices = circuit_obj.devices()
    return render(request, 'energize_andover/Circuit.html',
                  {'circuit': circuit_obj, 'Rooms': Rooms, 'school' : school, 'devices': devices})

def closet(request, closet_id):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
    closet_obj = get_object_or_404(Closet, pk=closet_id)
    panels = Panel.objects.filter(Closet__pk=closet_id)
    school = closet_obj.School
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if school not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    return render(request, 'energize_andover/Closet.html',
                  {'closet': closet_obj, 'panels': panels, 'school':school})

def adder(request):
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")
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
                users = form.cleaned_data['all_users']
                for user in users:
                    Usr = User.objects.filter(username = user).first()
                    SU = SpecialUser.objects.filter(User = Usr).first()
                    SU.Authorized_Schools.add(new)
                    SU.save()
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
    if (request.session.get('logged_in', None) == None):
        req = str(request).replace("/energize_andover", "")
        request.session['destination'] = req[req.index("/") + 1: len(req) - 2]
        return HttpResponseRedirect("Login")

    if request.method == 'GET':
        current_school = request.GET.get('school')
        school_obj = School.objects.filter(Name=current_school).first()
        user = authenticate(username=request.session['username'], password=request.session['password'])
        if user is not None:
            su = SpecialUser.objects.filter(User=user).first()
            if School.objects.filter(Name= current_school).first() not in su.Authorized_Schools.all():
                return HttpResponseRedirect("electric")
        form = SearchForm(request.GET, request.FILES)
        if form.is_valid():

            print(current_school)
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
                        if title.lower() == all_panels[i].Name[0:len(title)].lower() and all_panels[i].School.Name.lower() == current_school.lower():
                            #print(all_panels[i])
                            panels.append(all_panels[i])
                    except:
                        None
            if request.GET.get('circuits') == 'on':
                all_devices = Device.objects.all()
                school = School.objects.filter(Name=current_school).first()
                all_devs = school.devices()
                for i in range(0, len(all_devices)):
                    try:

                        #print (school.Name)
                        if title.lower() in all_devices[i].Name.lower() and all_devices[i] in all_devs:
                            circuits.append(all_devices[i])
                    except Exception as e:
                        print (e)
                all_circuits = Circuit.objects.all()
                devs = []
                for i in range (0, len(all_circuits)):
                    try:
                        if title.lower() in all_circuits[i].Name.lower() and all_circuits[i].Panel.School.Name.lower() == current_school.lower():
                            #print (title)
                           # print ("a")
                            #print (all_circuits[i])
                            circ_devices = all_circuits[i].devices()
                            #print (circ_devices)
                            for j in range(0, len(circ_devices)):
                                if not circ_devices[j] in circuits:
                                    circuits.append(circ_devices[j])
                    except Exception as e:
                        print (e)
                #for i in range(0, len(circuits)):
                #print (circuits[0])
            if request.GET.get('rooms') == 'on':
                all_rooms = Room.objects.all()
                for i in range(0, len(all_rooms)):
                    try:
                        if title.lower() == all_rooms[i].Name.lower() and all_rooms[i].School.Name.lower() == current_school.lower():
                            # print(all_panels[i])
                            rooms.append(all_rooms[i])
                    except:
                        None
                    try:
                        if title.lower() == all_rooms[i].OldName.lower() and all_rooms[i].School.Name.lower() == current_school.lower():
                            rooms.append(all_rooms[i])
                    except:
                        None
                    try:
                        if title.lower() in all_rooms[i].Type.lower() and all_rooms[i].School.Name.lower() == current_school.lower():
                            rooms.append(all_rooms[i])
                    except:
                        None
            if request.GET.get('closets') == 'on':
                all_closets = Closet.objects.all()
                for i in range(0, len(all_closets)):
                    try:
                        if title.lower() == all_closets[i].Name.lower() and all_closets[i].School.Name.lower() == current_school.lower():
                            # print(all_panels[i])
                            closets.append(all_closets[i])
                    except:
                        None
                    try:
                        if title.lower() == all_closets[i].Old_Name.lower() and all_closets[i].School.Name.lower() == current_school.lower():
                            closets.append(all_closets[i])
                    except:
                        None
            return render(request, 'energize_andover/Search.html', {'form': form, 'title': title,
                            'panels': panels, 'circuits': circuits, 'rooms': rooms, 'closets': closets, 'school':current_school, 'schoo':school_obj})
        return render(request, 'energize_andover/Search.html', {'form': form, 'title': "", 'school':current_school,'schoo':school_obj})
    else:
        form = SearchForm()
        current_school = request['school']
        school_obj = School.objects.filter(Name = current_school).first()
    return HttpResponse(render(request, 'energize_andover/Search.html', context = {'form': form, 'title': "", 'school':current_school, 'schoo': school_obj}))

def dictionary (request):
    return render(request, 'energize_andover/Dictionary.html')

def login (request):
    if request.method == "GET":
        form = LoginForm(request.GET, request.FILES)
        if form.is_valid():
            print(True)
            if request.GET.get('username') is None or request.GET.get("password") is None:
                return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form,
                                                                                    'message': "Login Failed: Missing Username and/or Password"}))
            user = authenticate(username=request.GET.get('username'), password=request.GET.get('password'))
            if user is not None:
                request.session['logged_in'] = True
                request.session['username'] = request.GET.get('username')
                request.session['password'] = request.GET.get('password')
                schools = School.objects.filter()
                if request.session.get('destination', None) == None:
                    return HttpResponseRedirect('electric')
                dest_string = request.session['destination']
                request.session['destination'] = None
                return HttpResponseRedirect(dest_string)
            else:
                return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form, 'message': "Login Failed: Incorrect Username and/or Password"}))
        return HttpResponse(render(request, 'energize_andover/Login.html', {'form': form}))


def logout (request):
    #print (request.GET.get('mybtn'))
    if (request.GET.get('mybtn')):
        request.session['logged_in'] = None
        request.session['username'] = None
        request.session['password'] = None
        return HttpResponseRedirect("Login")

def user_creation(request):
    if request.method == "GET":
        form = NewUserForm(request.GET, request.FILES)
        if form.is_valid():
            user = authenticate(username=request.GET.get('master_username'), password=request.GET.get('master_password'))
            if user is not None and Permission.objects.filter(codename = "can_create_user").first() in user.user_permissions.all():
                schools = form.cleaned_data['approved_schools']
                if request.GET.get('username') is not None and request.GET.get('password') is not None and request.GET.get('email') is not None:
                    new_user = User.objects.create_user(username=request.GET.get('username'),
                                     password=request.GET.get('password'), email=request.GET.get('email'))
                    new_user.save()
                    schools_user = SpecialUser(User = new_user)
                    schools_user.save()
                    for i in schools:
                        schoo = School.objects.filter(Name = i).first()
                        schools_user.Authorized_Schools.add(schoo)
                    schools_user.save()
                    return HttpResponseRedirect('Login')
                else:
                    return render(request, 'energize_andover/UserCreation.html', {'form': form, 'message': "Missing Username, Password, or Email"})
            else:
                return render(request, 'energize_andover/UserCreation.html', {'form': form, 'message': "Incorrect Administrator Username and/or Password"})
        return render(request, 'energize_andover/UserCreation.html', {'form': form})

def user_management(request):
    user_list = User.objects.all()
    usrs = []
    for user in user_list:
        if Permission.objects.filter(codename = "can_create_user").first() not in user.user_permissions.all():
            usrs.append(user)
    if request.method == "GET":
        for usr in usrs:
            if (request.GET.get(usr.username)) == "Delete":
                usr.delete()
                return HttpResponseRedirect('Management')
            elif (request.GET.get(usr.username)) == "Edit":
                spec_usr = SpecialUser.objects.filter(User = usr).first()
                schools = School.objects.all()
                permissions = Permission.objects.all()
                return HttpResponse(render(request, 'energize_andover/UserEditing.html', {'user': usr, 'schools': schools, 'su':spec_usr, 'permissions': permissions}))
    return HttpResponse(render(request, 'energize_andover/UserManagement.html', {'users': usrs}))

def user_editing(request):
    if request.GET.get('save'):
        print('True')
        user = request.GET.get('user')
        for school in School.objects.all():
            print (request.GET.get(school.Name))
        return HttpResponseRedirect("Management")
    return HttpResponse(render(request, 'energize_andover/UserEditing.html'))
"""
ct = ContentType.objects.get_for_model(User)
permission = Permission.objects.create(codename = "can_create_user",
                                       name = "Can Create User",
                                       content_type = ct)
permission.save()
User.objects.filter(username = "energizeandover").first().user_permissions.add(permission)
"""
