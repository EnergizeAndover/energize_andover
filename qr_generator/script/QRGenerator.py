import os
import pyqrcode
from django.shortcuts import get_object_or_404
from energize_andover.models import School
from qr_generator.script import LabelGenerator

def generate(school_id, rooms=False, panels=False, closets=False):
    school_obj = get_object_or_404(School, pk=school_id)
    os.chdir('/var/www/gismap/qr_generator')

    if os.path.exists('room_codes.pdf'):
        os.remove('room_codes.pdf')
    if os.path.exists('panel_codes.pdf'):
        os.remove('panel_codes.pdf')
    if os.path.exists('closet_codes.pdf'):
        os.remove('closet_codes.pdf')

    if(rooms):
        path = 'temp_rooms'
        if not os.path.exists(path):
            os.makedirs(path)

        os.chdir('temp_rooms')
        rooms = school_obj.rooms().order_by("QID")
        for room in rooms:
            url = pyqrcode.create("http://energizeandover.hopto.org:8080/energize_andover/QRCode/School"+str(school_id)+"/Room"+str(room.QID))
            url.png('Room'+str(room.QID)+'.png', scale=6, module_color=[0, 0, 0, 0], background=[0xff, 0xff, 0xff])

        os.chdir("..")

    if (panels):
        path = 'temp_panels'
        if not os.path.exists(path):
            os.makedirs(path)

        os.chdir('temp_panels')
        panels = school_obj.panels().order_by("QID")
        for panel in panels:
            url = pyqrcode.create("http://energizeandover.hopto.org:8080/energize_andover/QRCode/School"+str(school_id)+"/Panel"+str(panel.QID))
            url.png('Panel'+str(panel.QID)+'.png', scale=6, module_color=[0, 0, 0, 0], background=[0xff, 0xff, 0xff])

        os.chdir("..")

    if (closets):
        path = 'temp_closets'
        if not os.path.exists(path):
            os.makedirs(path)

        os.chdir('temp_closets')
        closets = school_obj.closets().order_by("QID")
        for closet in closets:
            url = pyqrcode.create("http://energizeandover.hopto.org:8080/energize_andover/QRCode/School"+str(school_id)+"/Closet"+str(closet.QID))
            url.png('Closet'+str(closet.QID)+'.png', scale=6, module_color=[0, 0, 0, 0], background=[0xff, 0xff, 0xff])

        os.chdir("..")

    LabelGenerator.generate(school_id)