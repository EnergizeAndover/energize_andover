from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from login.views import check_status, check_admin
from energize_andover.forms import *
from school_editing.forms import *


def electrical_mapping(request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    for a_school in School.objects.all():
        if request.POST.get(a_school.Name):
            a_school.delete()
    if request.method == 'POST':
        if request.POST.get('Start'):
            return HttpResponseRedirect('Populate')
        if request.POST.get('Manage'):
            return HttpResponseRedirect('Management')
    if (request.GET.get('mybtn')):
        request.session['logged_in'] = None
        return HttpResponseRedirect("Login")
    schools = School.objects.filter()
    if_admin = check_admin(request)
    return render(request, 'energize_andover/Electrical.html',
                  {'title': 'School Select', 'schools': schools, 'if_admin': if_admin})

def school(request, school_id):
    if check_status(request) is False:
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
        devices = Device.objects.none()

    return render(request, 'energize_andover/School.html',
                  {'title': 'School Select', 'school': school_obj,
                   'Rooms': Rooms, 'Panels': Panels, 'Closets': Closets, 'Devices': devices,
                   'form': form})

def device(request, device_id):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    user = authenticate(username=request.session['username'], password=request.session['password'])
    device_ = get_object_or_404(Device, pk=device_id)
    rooms = device_.rooms()
    circuits = device_.circuits()
    circ = circuits.first()
    panel_ = circ.Panel
    school_ = circ.School
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if school_ not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    assoc_dev = device_.Associated_Device
    return render(request, 'energize_andover/Device.html',
                  {'device': device_, "room": rooms, 'school': school_, 'circuit': circuits, 'assoc_device': assoc_dev})

def panel(request, panel_id):
    if check_status(request) is False:
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
        for count in reversed(range(6)):
            for j in range(0, len(transformers)):
                if len(transformers[j].Name) == count:
                    if transformers[j].Name in path:
                        path = path.replace(transformers[j].Name, "")
        name = path[0: path.index(panel.Name) - 1]
        for j in range (0, len(parray)):
            if parray[j].FQN == name and parray[j] not in rarray:
                rarray.append(parray[j])
    for i in range(0, len(rarray)):
        parray.remove(rarray[i])
    if panel_obj.School is not None:
        school = panel_obj.School

    Main = Panel.objects.filter(Name='MSWB')
    if Main.count()>0:
        Main = Main[0]

    picture = "energize_andover/" + panel_obj.Name.replace(" ", "") + ".jpg"
    if request.POST.get("Edit"):
        print(request)
        form = PanelEditForm(request.POST)
        return HttpResponse(request, "energize_andover/Panel.html", {'form':form})
    return render(request, 'energize_andover/Panel.html',
                  {'panel' : panel_obj,
                   'Rooms': Rooms, 'Circuits': parray,
                   'Subpanels' : Panels, 'Main' : Main, 'school': school,
                   'picture' : picture})

def room(request, room_id):
    if check_status(request) is False:
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
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    Rooms = circuit_obj.rooms()
    school = circuit_obj.School
    user = authenticate(username=request.session['username'], password=request.session['password'])
    if user is not None:
        su = SpecialUser.objects.filter(User=user).first()
        if school not in su.Authorized_Schools.all():
            return HttpResponseRedirect("electric")
    devices = circuit_obj.devices()
    return render(request, 'energize_andover/Circuit.html',
                  {'circuit': circuit_obj, 'Rooms': Rooms, 'school' : school, 'devices': devices})

def closet(request, closet_id):
    if check_status(request) is False:
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


def search(request):
    if check_status(request) is False:
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
                            panels.append(all_panels[i])
                    except:
                        None
            if request.GET.get('circuits') == 'on':
                all_devices = Device.objects.all()
                school = School.objects.filter(Name=current_school).first()
                all_devs = school.devices()
                for i in range(0, len(all_devices)):
                    try:
                        if title.lower() in all_devices[i].Name.lower() and all_devices[i] in all_devs:
                            circuits.append(all_devices[i])
                    except Exception as e:
                        print (e)
                all_circuits = Circuit.objects.all()
                devs = []
                for i in range (0, len(all_circuits)):
                    try:
                        if title.lower() in all_circuits[i].Name.lower() and all_circuits[i].School.Name.lower() == current_school.lower():
                            circ_devices = all_circuits[i].devices()

                            for j in range(0, len(circ_devices)):
                                if not circ_devices[j] in circuits:
                                    circuits.append(circ_devices[j])
                    except Exception as e:
                        print (e)

            if request.GET.get('rooms') == 'on':
                all_rooms = Room.objects.all()
                for i in range(0, len(all_rooms)):
                    try:
                        if title.lower() == all_rooms[i].Name.lower() and all_rooms[i].School.Name.lower() == current_school.lower():
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

