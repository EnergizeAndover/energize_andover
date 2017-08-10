import os

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from login.views import check_status, School
from qr_generator.script import QRGenerator

def generator(request):
    if check_status(request) is False:
        return HttpResponseRedirect("Login")
    schools = School.objects.filter()
    for school in School.objects.all():
        if request.POST.get(str(school.id)):
            return render(request, 'energize_andover/QRGenerator.html',
                  {'school': school.id, 'selected': True})
    if request.POST.get("Generate"):
        QRGenerator.generate(school.id, rooms=request.POST.get("Rooms"), panels=request.POST.get("Panels"), closets=request.POST.get("Closets"))
        os.chdir('/var/www/gismap/qr_generator')
        room = False
        panel = False
        closet = False
        if os.path.exists('room_codes.pdf'):
            room = True
        if os.path.exists('panel_codes.pdf'):
            panel = True
        if os.path.exists('closet_codes.pdf'):
            closet = True
        os.chdir('..')
        return render(request, 'energize_andover/QRGenerator.html', {'generate': True, 'rooms': room, 'panels': panel, 'closets': closet})
    return render(request, 'energize_andover/QRGenerator.html', {'schools': schools})

def open_rooms(request):
    os.chdir('/var/www/gismap/qr_generator')
    with open('room_codes.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=room_codes.pdf'
        os.chdir('..')
        return response

def open_panels(request):
    os.chdir('/var/www/gismap/qr_generator')
    with open('panel_codes.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=panel_codes.pdf'
        os.chdir('..')
        return response

def open_closets(request):
    os.chdir('/var/www/gismap/qr_generator')
    with open('closet_codes.pdf', 'rb') as pdf:
        response = HttpResponse(pdf.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'filename=closet_codes.pdf'
        os.chdir('..')
        return response