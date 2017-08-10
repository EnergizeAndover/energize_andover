from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import Room, Panel, Closet, School


# Create your views here.
def qr_rooms_redirect(request, qr_id, school_id):
    school_obj = get_object_or_404(School, pk=school_id)
    room_obj = school_obj.rooms().get(QID=qr_id)
    return HttpResponseRedirect("/energize_andover/Room"+str(room_obj.pk))

def qr_panels_redirect(request, qr_id, school_id):
    school_obj = get_object_or_404(School, pk=school_id)
    panel_obj = school_obj.panels().get(QID=qr_id)
    return HttpResponseRedirect("/energize_andover/Panel"+str(panel_obj.pk))

def qr_closets_redirect(request, qr_id, school_id):
    school_obj = get_object_or_404(School, pk=school_id)
    closet_obj = school_obj.closets().get(QID=qr_id)
    return HttpResponseRedirect("/energize_andover/Closet"+str(closet_obj.pk))