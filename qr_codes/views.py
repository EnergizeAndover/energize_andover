from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from energize_andover.models import Room, Panel, Closet

# Create your views here.
def qr_rooms_redirect(request, qr_id):
    room_obj = get_object_or_404(Room, QID=qr_id)
    print("Closet")
    return HttpResponseRedirect("/energize_andover/Room"+str(room_obj.pk))

def qr_panels_redirect(request, qr_id):
    panel_obj = get_object_or_404(Panel, QID=qr_id)
    print("Panel")
    return HttpResponseRedirect("/energize_andover/Panel"+str(panel_obj.pk))

def qr_closets_redirect(request, qr_id):
    closet_obj = get_object_or_404(Closet, QID=qr_id)
    return HttpResponseRedirect("/energize_andover/Closet"+str(closet_obj.pk))