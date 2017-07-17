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
    # if request.GET.get("Adder"):
    #    return render(request, "energize_andover/Adder.html", {'school_choice': school_obj})
    if type == "closets":
        model_obj = school_obj.closets().order_by('id')
    elif type == "panels":
        model_obj = school_obj.panels().order_by('id')
    elif type == "rooms":
        model_obj = school_obj.rooms().order_by('id')
    else:
        model_obj = school_obj.devices().order_by('id')

    form = SearchForm()

    picture = "energize_andover/" + school_obj.Name + ".jpg"
    #if not os.path.isfile(picture):
    #    picture = None
    return render(request, 'energize_andover/TableSort.html',
                  {'title': 'Table Sorting', 'type': type, 'school': school_obj,
                   'model_obj': model_obj, 'form': form})

