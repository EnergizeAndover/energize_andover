from django.contrib.auth import authenticate
from django.contrib.auth.models import Permission
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from login.views import check_status, check_admin, check_school_privilege, logout
from energize_andover.forms import *
from school_editing.forms import *
import os.path

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
        logout(request)
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
    if check_school_privilege(school_obj, request) == False:
        return HttpResponseRedirect("electric")
    #if request.GET.get("Adder"):
    #    return render(request, "energize_andover/Adder.html", {'school_choice': school_obj})
    Closets = school_obj.closets().order_by('id')
    Panels = school_obj.panels().order_by('id')
    Rooms = school_obj.rooms().order_by('id')
    form = SearchForm()
    devices = school_obj.devices().order_by('id')
    if len(devices) == 0:
        devices = Device.objects.none()
    picture = "energize_andover/" + school_obj.Name + ".jpg"
    #if not os.path.isfile(picture):
    #    picture = None
    return render(request, 'energize_andover/School.html',
                  {'title': 'School Select', 'school': school_obj,
                   'Rooms': Rooms, 'Panels': Panels, 'Closets': Closets, 'Devices': devices, 'picture': picture,
                   'form': form})

def device(request, device_id):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    device_ = get_object_or_404(Device, pk=device_id)
    rooms = device_.rooms()
    circuits = device_.circuits()
    circ = circuits.first()
    school_=device_.School
    #print(school_)
    #print(SpecialUser.objects.get(User = User.objects.get(username= request.session['username'])).Authorized_Schools.all())
    if check_school_privilege(school_, request) == False:
        return HttpResponseRedirect("electric")
    assoc_dev = device_.Associated_Device
    if request.POST.get("Edit"):
        # print(request)
        form = PanelEditForm(request.POST)
        return HttpResponse(request, "energize_andover/Device.html", {'device': device_, 'form': form})
    return render(request, 'energize_andover/Device.html',
                  {'device': device_, "room": rooms, 'school': school_, 'circuit': circuits, 'assoc_device': assoc_dev})

def panel(request, panel_id):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")

    panel_obj = get_object_or_404(Panel, pk=panel_id)
    if check_school_privilege(panel_obj.School, request) == False:
        return HttpResponseRedirect("electric")
    if panel_obj.rooms() is not None:
        Rooms = panel_obj.rooms()
    if panel_obj.circuits() is not None:
        Circuits = panel_obj.circuits().order_by('id')
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
    #if not os.path.exists(picture):
        #picture = None
    if request.POST.get("Edit"):
        #print(request)
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
    if check_school_privilege(School, request) == False:
        return HttpResponseRedirect("electric")
    Panels = room_obj.panels().order_by('id')
    Circuits = room_obj.circuits()

    #Circuits = Circuit.objects.filter(Rooms = room_obj)
    if request.POST.get("Edit"):
        #print(request)
        form = PanelEditForm(request.POST)
        return HttpResponse(request, "energize_andover/Room.html", {'form':form})
    return render (request, 'energize_andover/Room.html',
                   {'room' : room_obj,
                    "school": School,
                    'Panels': Panels,
                    'Circuits': Circuits})

def circuit(request, circuit_id):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    Rooms = circuit_obj.rooms().order_by("id")
    school = circuit_obj.School
    if check_school_privilege(school, request) == False:
        return HttpResponseRedirect("electric")
    if request.POST.get("Edit"):
        #print(request)
        form = PanelEditForm(request.POST)
        return HttpResponse(request, "energize_andover/Circuit.html", {'form':form})
    devices = circuit_obj.devices().order_by('id')
    return render(request, 'energize_andover/Circuit.html',
                  {'circuit': circuit_obj, 'Rooms': Rooms, 'school' : school, 'devices': devices})

def closet(request, closet_id):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    closet_obj = get_object_or_404(Closet, pk=closet_id)
    panels = Panel.objects.filter(Closet__pk=closet_id).order_by('id')
    school = closet_obj.School
    if check_school_privilege(school, request) == False:
        return HttpResponseRedirect("electric")
    if request.POST.get("Edit"):
        # print(request)
        form = PanelEditForm(request.POST)
        return HttpResponse(request, "energize_andover/Closet.html", {'closet': closet_obj, 'form': form})
    return render(request, 'energize_andover/Closet.html',
                  {'closet': closet_obj, 'panels': panels, 'school':school})


def search(request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    if request.method == 'GET':
        current_school = request.GET.get('school')
        school_obj = School.objects.get(Name=current_school)
        if check_school_privilege(school_obj, request) == False:
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
                all_panels = Panel.objects.filter(School=school_obj).order_by('id')
                for i in range (0, len(all_panels)):
                    try:
                        if title.lower() == all_panels[i].Name[0:len(title)].lower():
                            panels.append(all_panels[i])
                    except:
                        None
            if request.GET.get('circuits') == 'on':
                all_devices = Device.objects.filter(School = school_obj).order_by('id')

                for i in range(0, len(all_devices)):
                    try:
                        if title.lower() in all_devices[i].Name.lower():
                            circuits.append(all_devices[i])
                    except Exception as e:
                        print (e)
                all_circuits = Circuit.objects.filter(School = school_obj).order_by('id')
                devs = []
                for i in range (0, len(all_circuits)):
                    try:
                        if title.lower() in all_circuits[i].Name.lower():
                            circ_devices = all_circuits[i].devices()

                            for j in range(0, len(circ_devices)):
                                if not circ_devices[j] in circuits:
                                    circuits.append(circ_devices[j])
                    except Exception as e:
                        print (e)

            if request.GET.get('rooms') == 'on':
                all_rooms = Room.objects.filter(School=school_obj).order_by('id')
                for i in range(0, len(all_rooms)):
                    try:
                        if title.lower() == all_rooms[i].Name.lower():
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
                all_closets = Closet.objects.filter(School=school_obj).order_by('id')
                for i in range(0, len(all_closets)):
                    try:
                        if title.lower() == all_closets[i].Name.lower():
                            closets.append(all_closets[i])
                    except:
                        None
                    try:
                        if title.lower() == all_closets[i].Old_Name.lower():
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



def changelog (request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    if check_admin(request) is False:
        return HttpResponseRedirect("electric")
    return render(request, 'energize_andover/ChangeLog.html')

