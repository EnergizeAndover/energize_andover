from django.shortcuts import render
from school_adder.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from school_adder.script.room_mapping import parse as RoomParse
from school_adder.script.circuit_room_mapping import parse as PanelParse
from school_adder.script.circuit_room_relationships import parse as DeviceParse
from login.views import check_status, check_school_privilege, check_admin, check_school_edit_privilege, update_log

def adder(request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    if check_school_edit_privilege(request) is False:
        return HttpResponseRedirect("School" + str(School.objects.get(Name = request.GET.get("school_choice")).id))
    if check_school_privilege(School.objects.get(Name = request.GET.get("school_choice")), request) == False:
        return HttpResponseRedirect("electric")
    if request.method == 'POST':
        #print (request.POST.get("School"))
        if request.POST.get('start'):
            print(request.POST)
            form = AdderTypeForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                if data['type'] == 'Closet':
                    form = ClosetForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'closet': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
                elif data['type'] == 'Panel':
                    form = PanelForm()
                    #form.Closet.queryset = Closet.objects.filter(School=request.GET.get(""))
                    return render(request, 'energize_andover/Adder.html',
                                  {'panel': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
                elif data['type'] == 'Room':
                    form = RoomForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'room': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
                elif data['type'] == 'Circuit':
                    form = CircuitForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'circuit': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
                elif data['type'] == 'Device':
                    form = DeviceForm()
                    return render(request, 'energize_andover/Adder.html',
                                  {'device': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})

        elif request.POST.get('closet'):
            form = ClosetForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.School = School.objects.get(Name=request.GET.get("school_choice"))
                new.save()
                message = "Closet " + new.Name + " added."
                update_log(message, new.School, request)
                form = AdderTypeForm()
                return HttpResponseRedirect("Closet" + str(new.pk))
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'closet': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
        elif request.POST.get('panel'):
            form = PanelForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.School = School.objects.get(Name = request.GET.get("school_choice"))
                new.FQN = new.Name
                new.save()
                message = "Panel " + new.Name + " added."
                update_log(message, new.School, request)
                form = AdderTypeForm()
                return HttpResponseRedirect("Panel" + str(new.pk))
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'panel': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
        elif request.POST.get('room'):
            form = RoomForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.School = School.objects.get(Name = request.GET.get("school_choice"))
                new.save()
                message = "Room " + new.Name + " added."
                update_log(message, new.School, request)
                form = AdderTypeForm()
                return HttpResponseRedirect("Room" + str(new.pk))
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'room': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
        elif request.POST.get('device'):
            form = DeviceForm(request.POST, request.FILES)
            if form.is_valid():
                new = form.save()
                new.School = School.objects.get(Name = request.GET.get("school_choice"))
                new.save()
                message = "Device " + new.Name + " added."
                update_log(message, new.School, request)
                form = AdderTypeForm()
                return HttpResponseRedirect("Device" + str(new.pk))
            else:
                return render(request, 'energize_andover/Adder.html',
                              {'device': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})
    form = AdderTypeForm()
    return render(request, 'energize_andover/Adder.html',
                  {'type': form, 'title': 'Electrical Mapping Creation', 'school_choice': request.GET.get("school_choice")})


def populate(request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    if check_admin(request) is False:
        return HttpResponseRedirect("electric")
    if request.method == 'POST':
        form = PopulationForm(request.POST, request.FILES)
        if form.is_valid():
            school = School(Name = form.cleaned_data['New_School'])
            school.save()
            usrs = form.cleaned_data['all_users']
            for usr in usrs:
                user = User.objects.filter(username = usr)
                su = SpecialUser.objects.filter(User=user).first()
                su.Authorized_Schools.add(school)
                su.save()
            RoomParse(form.cleaned_data['Room_File'], school)
            PanelParse(form.cleaned_data['Panel_File'], school)
            DeviceParse(form.cleaned_data['Device_File'], school)
            return render(request, 'energize_andover/Population.html', context={'school': school})
    else:
        form = PopulationForm()
    return render(request, 'energize_andover/Population.html',
                  {'form':form})

