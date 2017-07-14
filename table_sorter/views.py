from django.shortcuts import render, get_object_or_404
from login.views import check_status, check_school_privilege
from django.http import HttpResponse, HttpResponseRedirect
from energize_andover.models import School
from energize_andover.forms import *
from school_editing.forms import *


def list(request, school_id, type):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    school_obj = get_object_or_404(School, pk=school_id)
    if check_school_privilege(school_obj, request) is False:
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
    return render(request, 'energize_andover/Test.html',
                  {'title': 'Table Sorting', 'type': type, 'school': school_obj,
                   'Rooms': Rooms, 'Panels': Panels, 'Closets': Closets, 'Devices': devices, 'picture': picture,
                   'form': form})

