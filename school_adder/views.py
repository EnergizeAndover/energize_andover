from django.shortcuts import render
from school_adder.forms import *
from django.http import HttpResponse, HttpResponseRedirect
from school_adder.script.room_mapping import parse as RoomParse
from school_adder.script.circuit_room_mapping import parse as PanelParse
from school_adder.script.circuit_room_relationships import parse as DeviceParse
from login.views import check_status

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
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
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

