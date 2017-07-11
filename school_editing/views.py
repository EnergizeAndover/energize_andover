from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import *
from .forms import *
from energize_andover.forms import *
from login.views import check_status, check_school_edit_privilege, check_school_privilege, update_log


def panel_editing(request, panel_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    if check_school_edit_privilege(request) is False:
        return HttpResponseRedirect("/energize_andover/Panel" + panel_id)
    panel_obj = get_object_or_404(Panel, pk=panel_id)
    if check_school_privilege(panel_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    form = PanelEditForm(initial={'Name': panel_obj.Name})
    try:
        par_circuits = panel_obj.Panels.circuits()
    except:
        par_circuits = None
    selected_panel = panel_obj.Panels
    changed = False
    if request.POST.get("Save Name"):
        message = "Panel Name Change: " + panel_obj.Name + " -->" + request.POST.get(
            "Name") + ". All Affected Circuits and Panels renamed accordingly. "
        update_log(message, panel_obj.School, request)
        name = panel_obj.Name
        new_name = request.POST.get("Name")
        panel_obj.Name = new_name
        panel_obj.FQN = panel_obj.FQN.replace(name, new_name)
        panel_obj.save()
        panels = Panel.objects.filter(School = panel_obj.School)
        for pan in panels:
            if ("." + name + ".") in pan.FQN:
                pan.FQN = pan.FQN.replace(name, request.POST.get("Name"))
                pan.save()
        circuits = Circuit.objects.filter(School = panel_obj.School)
        for circ in circuits:
            if ("." + name + ".") in circ.FQN:
                circ.FQN = circ.FQN.replace(name, request.POST.get("Name"))
                circ.save()
            if ("." + name + ".") in circ.Name:
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
    if request.POST.get("Add Circuits"):
        number = int(request.POST.get("Additional Circuits"))
        message = str(number)  + " Circuits added to Panel " + panel_obj.Name
        update_log(message, panel_obj.School, request)
        circs = Circuit.objects.filter(Panel=panel_obj)
        current_circ_numb = circs.count()
        for i in range(0, number):
            new_number = i + current_circ_numb + 1
            new_circuit = Circuit(Name = panel_obj.Name + "." + str(new_number), Number = new_number, FQN = panel_obj.FQN + "." + str(new_number), Panel = panel_obj, School = panel_obj.School)
            new_circuit.save()
    if request.POST.get("Save Parent"):
        selected_panel = Panel.objects.filter(School=panel_obj.School).get(id=request.POST.get("Panels"))
        par_circuits = selected_panel.circuits()
        changed = True
    if request.POST.get("Save Circuit"):
        new_par_pan = request.POST.get("Selected Panel")
        circ = Circuit.objects.filter(School=panel_obj.School).get(id=request.POST.get("Circuit"))
        try:
            par_pan = panel_obj.Panels.Name
            message = "Parent Panel Change on " + panel_obj.Name + ": " + par_pan  + " -->" + new_par_pan + ". All Affected Circuits and Panels renamed accordingly. "
        except:
            message = "Parent Panel for " + panel_obj.Name + " set to " + new_par_pan
        update_log(message, panel_obj.School, request)
        panel_obj.Panels = Panel.objects.filter(School=panel_obj.School).get(Name = new_par_pan)
        panel_obj.save()
        new_par_fqn = Panel.objects.filter(School=panel_obj.School).get(Name = new_par_pan).FQN
        for panel in Panel.objects.filter(School=panel_obj.School):
            if ("." + panel_obj.Name + ".") in panel.FQN or panel.FQN.find(panel_obj.Name + ".")==0 or panel_obj == panel:
                breakpt = panel.FQN.index(panel_obj.Name)
                remainder = panel.FQN[breakpt:]
                panel.FQN = new_par_fqn + "." + str(circ.Number) + "." + remainder
                panel.save()
        #panel_obj = Panel.objects.get(Name = panel_obj.Name)
        for circuit in Circuit.objects.filter(School = panel_obj.School):
            if ("." + panel_obj.Name + ".") in circuit.FQN or circuit.FQN.find(panel_obj.Name + ".")==0 or circuit.Panel == panel_obj:
                print (circuit.FQN)
                circuit.FQN = circuit.Panel.FQN + "." + circuit.Number
                circuit.save()

    if request.POST.get("Save Closet"):
        message = "Panel Closet Change: " + panel_obj.Closet + " -->" + request.POST.get("Closet")
        update_log(message, panel_obj.School, request)
        panel_obj.Closet = Closet.objects.filter(School=panel_obj.School).get(id=request.POST.get("Closet"))
        panel_obj.save()
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Panel " + panel_obj.Name + " Deleted. All Circuits also Deleted"
            update_log(message, panel_obj.School, request)
            parent = panel_obj.Panels
            for circuit in panel_obj.circuits():
                circuit.delete()
            school_obj = panel_obj.School
            panels = panel_obj.panels()
            for pan in panels:
                #print(pan.Name)
                pan.Panels = None
                #print (pan.Panels)
                pan.save()
            for pan in Panel.objects.filter(School = panel_obj.School):
                if ("." + panel_obj.Name + ".") in pan.FQN:# and not pan == panel_obj:
                    try:
                        print(pan.FQN)
                        index1 = pan.FQN.index(panel_obj.Name) + len(panel_obj.Name)+1
                        new_index = pan.FQN.index('.', index1)
                        pan.FQN = pan.FQN[new_index + 1:]
                        pan.save()
                    except:
                        None
            for circuit in Circuit.objects.filter(School = panel_obj.School):
                if ("." + panel_obj.Name + ".") in circuit.FQN:
                    try:
                        index1 = circuit.FQN.index(panel_obj.Name) + len(panel_obj.Name) + 1
                        new_index = circuit.FQN.index(".", index1)
                        circuit.FQN = circuit.FQN[new_index + 1:]
                        circuit.save()
                    except:
                        None

            panel_obj.delete()
            if not parent == None:
                return HttpResponseRedirect("/energize_andover/Panel" + str(parent.pk))
            else:
                return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))

    return HttpResponse(render(request, 'energize_andover/Panel.html',
                  {'panel': panel_obj,
                   'form': form,
                   'Panels': Panel.objects.filter(School = panel_obj.School),
                   'selected': selected_panel,
                   'par_circuits': par_circuits,
                   'changed': changed,
                   'Closets': Closet.objects.filter(School = panel_obj.School)}))

def room_editing (request, room_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    if check_school_edit_privilege(request) is False:
        return HttpResponseRedirect("/energize_andover/Room" + room_id)
    room_obj = get_object_or_404(Room, pk=room_id)
    if check_school_privilege(room_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
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
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Room " + room_obj.Name + " Deleted."
            update_log(message, room_obj.School, request)
            school_obj = room_obj.School
            for device in Device.objects.filter(Room = room_obj):
                device.Room = None
                device.save()
            room_obj.delete()
            return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))
    form = PanelEditForm(initial={'Name': room_obj.Name})
    return HttpResponse(render(request, "energize_andover/Room.html", {'room': room_obj,
                                                                       'form': form}))
                                                                       #'Panels': Panel.objects.filter(School=room_obj.School),
                                                                       #'room_panels': room_obj.Panels.all()}))

def device_editing(request, device_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    if check_school_edit_privilege(request) is False:
        return HttpResponseRedirect("/energize_andover/Device" + device_id)
    device_obj = get_object_or_404(Device, pk = device_id)
    if check_school_privilege(device_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    form = PanelEditForm(initial={'Name': device_obj.Name})
    if request.POST.get("Save Name"):
        message = "Device Name Change: " + device_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, device_obj.School, request)
        device_obj.Name = request.POST.get("Name")
        device_obj.save()
    if request.POST.get("Save Power"):
        message = "Device Power Change: " + device_obj.Power + " -->" + request.POST.get("Power")
        update_log(message, device_obj.School, request)
        device_obj.Power = request.POST.get("Power")
        device_obj.save()
    if request.POST.get("Save Zone"):
        message = "Device Zone Change: " + device_obj.Location + " -->" + request.POST.get("Zone")
        update_log(message, device_obj.School, request)
        device_obj.Location = request.POST.get("Zone")
        device_obj.save()
    if request.POST.get("Save Notes"):
        message = "Device Notes Change: " + device_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, device_obj.School, request)
        device_obj.Notes = request.POST.get("Notes")
        device_obj.save()
    query = "Enter Query (Name of Device)     |"
    devices = []
    if request.POST.get("Search"):
        query = request.POST.get("Associated_Device_Query")
        devs = Device.objects.filter(School = device_obj.School)
        for dev in devs:
            if query.lower() == dev.Name.lower():
                devices.insert(0, dev)
            elif query.lower() in dev.Name.lower():
                devices.append(dev)
    if request.POST.get("Save Associated Device"):
        dev_id = request.POST.get("Associated_Dev")
        assoc_dev = Device.objects.filter(School=device_obj.School).get(id= dev_id)
        message = device_obj.to_string() + " is now associated with " + assoc_dev.to_string() +"."
        update_log(message, device_obj.School, request)
        device_obj.Associated_Device = assoc_dev
        device_obj.save()
        assoc_dev.Associated_Device = device_obj
        assoc_dev.save()
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Device " + device_obj.to_string() + " Deleted."
            update_log(message, device_obj.School, request)
            school_obj = device_obj.School
            device_obj.delete()
            return HttpResponseRedirect("/energize_andover/School" + str(school_obj.pk))
    return HttpResponse(render(request, "energize_andover/Device.html", {'device': device_obj,
                                                                        'devices': devices,
                                                                         'query':query,
                                                                         'form': form}))

def circuit_editing (request, circuit_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    if check_school_edit_privilege(request) is False:
        return HttpResponseRedirect("/energize_andover/Circuit" + circuit_id)
    circuit_obj = get_object_or_404(Circuit, pk=circuit_id)
    if check_school_privilege(circuit_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")
    if request.POST.get("Save Name"):
        message = "Circuit Name Change: " + circuit_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, circuit_obj.School, request)
        circuit_obj.Name = request.POST.get("Name")
        circuit_obj.save()
    if request.POST.get("Save Number"):
        message = "Circuit Number Change: " + circuit_obj.Number + " -->" + request.POST.get("Number")
        update_log(message, circuit_obj.School, request)
        circuit_obj.Number = request.POST.get("Number")
        circuit_obj.save()
    if request.POST.get("Save Notes"):
        message = "Circuit Notes Change: " + circuit_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, circuit_obj.School, request)
        circuit_obj.Notes = request.POST.get("Notes")
        circuit_obj.save()
    query = "Enter Query (Name of Device)     |"
    devices = []
    for dev in circuit_obj.devices():
        if request.POST.get(str(dev.id)):
            message = "Circuit-Device Change: Device " + dev.Name + " removed from Circuit " + circuit_obj.Name
            update_log(message, circuit_obj.School, request)
            dev.Circuit.remove(circuit_obj)
            try:
                remove = True
                for device in circuit_obj.devices():
                    if dev.Room == device.Room:
                        remove = False
                if remove:
                    circuit_obj.Rooms.remove(dev.Room)
                    circuit_obj.save()
                panel = circuit_obj.Panel
                remove = True
                room = dev.Room
                for circuit in panel.circuits():
                    if not circuit == circuit_obj:
                        for device in circuit.devices():
                            try:
                                if device.Room == room:
                                    print (circuit)
                                    remove = False
                            except:
                                None
                if remove:
                    room.Panels.remove(panel)
                    room.save()
            except:
                None
            #dev.save()
    if request.POST.get("Search"):
        query = request.POST.get("Device_Query")
        devs = Device.objects.filter(School=circuit_obj.School)
        for dev in devs:
            if query.lower() == dev.to_string().lower():
                devices.insert(0, dev)
            elif query.lower() in dev.to_string().lower():
                devices.append(dev)
    if request.POST.get("Add Device"):
        dev_id = request.POST.get("Device")
        added_dev = Device.objects.filter(School=circuit_obj.School).get(id= dev_id)
        message = "Device " + added_dev.to_string() + " added to Circuit " + circuit_obj.Name +"."
        update_log(message, circuit_obj.School, request)
        added_dev.Circuit.add(circuit_obj)
        added_dev.save()
        try:
            circuit_obj.Rooms.add(added_dev.Room)
            circuit_obj.save()
            panel = circuit_obj.Panel
            room = added_dev.Room
            room.Panels.add(panel)
            room.save()
        except:
            None
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Circuit " + circuit_obj.Name + " Deleted."
            update_log(message, circuit_obj.School, request)
            school_obj = circuit_obj.School
            #print(Device.objects.filter(Circuit=circuit_obj))
            for device in Device.objects.filter(Circuit=circuit_obj):
                print(device.Circuit.all())
                device.Circuit.remove(circuit_obj)
                device.save()
                print(device.Circuit.all())
            panel = circuit_obj.Panel
            circuit_obj.delete()
            return HttpResponseRedirect("/energize_andover/Panel" + str(panel.pk))
    form = PanelEditForm(initial={'Name': circuit_obj.Name})
    return HttpResponse(render(request, "energize_andover/Circuit.html", {'circuit': circuit_obj,
                                                                          'devices': circuit_obj.devices(),
                                                                          'search_devices': devices,
                                                                          'query':query,
                                                                         'form': form}))

def closet_editing(request, closet_id):
    if check_status(request) is False:
        return HttpResponseRedirect("/energize_andover/Login")
    if check_school_edit_privilege(request) is False:
        return HttpResponseRedirect("/energize_andover/Closet" + closet_id)
    closet_obj = get_object_or_404(Closet, pk=closet_id)
    if check_school_privilege(closet_obj.School, request) == False:
        return HttpResponseRedirect("/energize_andover/electric")

    if request.POST.get("Save Name"):
        message = "Closet Number Change: " + closet_obj.Name + " -->" + request.POST.get("Name")
        update_log(message, closet_obj.School, request)
        closet_obj.Name = request.POST.get("Name")
        closet_obj.save()
    if request.POST.get("Save Old Name"):
        message = "Old Closet Number Change: " + closet_obj.Old_Name + " -->" + request.POST.get("Old Name")
        update_log(message, closet_obj.School, request)
        closet_obj.Old_Name = request.POST.get("Old Name")
        closet_obj.save()
    if request.POST.get("Save Notes"):
        message = "Closet Notes Change: " + closet_obj.Notes + " -->" + request.POST.get("Notes")
        update_log(message, closet_obj.School, request)
        closet_obj.Notes = request.POST.get("Notes")
        closet_obj.save()
    if request.POST.get("Add Panel"):
        pan = Panel.objects.filter(School=closet_obj.School).get(pk=request.POST.get("Panels"))
        try:
            message = "Panel " + pan.Name + " moved from Closet " + pan.Closet.Name + " to Closet " +  closet_obj.Name
        except:
            message = "Panel " + pan.Name + " moved to Closet " +  closet_obj.Name
        update_log(message, closet_obj.School, request)
        pan.Closet = closet_obj
        pan.save()
    for panel in Panel.objects.filter(Closet = closet_obj):
        if request.POST.get(panel.Name):
            panel.Closet = None
            panel.save()
            message = "Panel " + panel.Name + " removed from Closet " + closet_obj.Name
            update_log(message, closet_obj.School, request)
    form = PanelEditForm(initial={'Name': closet_obj.Name})
    if request.POST.get("Confirm"):
        if request.POST.get("Username")==request.session['username'] and request.POST.get("Password")==request.session['password']:
            message = "Closet " + closet_obj.Name + " Deleted."
            update_log(message, closet_obj.School, request)
            school_obj = closet_obj.School
            for panel in Panel.objects.filter(Closet=closet_obj):
                panel.Closet = None
                panel.save()
            closet_obj.delete()
            return HttpResponseRedirect("/energize_andover/School"+str(school_obj.pk))

    return HttpResponse(render(request, "energize_andover/Closet.html", {'closet': closet_obj,
                                                                         'clos_panels': Panel.objects.filter(Closet = closet_obj).filter(School=closet_obj.School),
                                                                         'Panels': Panel.objects.filter(School = closet_obj.School),
                                                                          'form': form}))
