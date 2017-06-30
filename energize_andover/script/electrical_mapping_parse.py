import pandas as pd
import numpy as np
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *
#from energize_andover.forms import *


TEMPORARY_INPUT_FILENAME = '/var/www/gismap/mappingdata.csv'

def create_mapping(form_data):
    _save_input_file(form_data)
    parse(_temporary_input_file_path())



def _temporary_input_file_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)

def _save_input_file(temporary_file):
#    Save the uploaded file to disk so it can be handled
    with open(_temporary_input_file_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)


def parse (file):
    df = pd.read_csv(file)
    #print (df)
    df = df.fillna("")
    conversion = {}
    for int in range(0, df.columns.size):
        conversion[df.columns[int]] = int
    for i in range (1, len(df['School']) + 1):
        school = df._slice(slice(i-1,i))['School']
        closets = df._slice(slice(i-1,i))['Closets']
        panels = df._slice(slice(i-1,i))['Panels']
        circuits = df._slice(slice(i-1,i))['Circuits']
        new_room_number = df._slice(slice(i-1,i))['New Room #']
        old_room_number = df._slice(slice(i-1,i))['Old Room #']
        school = str(school)
        closets = str(closets)
        panels = str(panels)
        circuits = str(circuits)
        new_room_number = str(new_room_number)
        old_room_number = str(old_room_number)
        #print (school)

        school = school[5: school.index('\n')]
        closets = closets[5: closets.index('\n')]
        panels = panels[5: panels.index('\n')]
        circuits = circuits[5: circuits.index('\n')]
        new_room_number = new_room_number[5: new_room_number.index('\n')]
        old_room_number = old_room_number[5: old_room_number.index('\n')]
        new_closet = Closet(Name=new_room_number, School=school)
        new_closet.save()
        print("apple")
        print ("School: %s, Closets: %s, Panels: %s, Circuits: %s, New #: %s, Old #, %s" % (school, closets, panels, circuits, new_room_number, old_room_number))















""""
def parse(file, school):
    df = pd.read_csv(file)
    df = df.fillna('')
    df.index = df['Closet # (Old)']
    for closet in df.index:
        panels = df['Panel'][closet]
        voltages = df['Voltage'][closet]
        new_number = df['Closet # (New)'][closet]

        if type(panels) == str:
            panels = [panels]
            voltages = [voltages]
        else:
            voltages = voltages.tolist()
        if not type(new_number) == str:
            new_number = new_number.tolist()
            new_number = new_number[0]
        if not closet == '':
            old_closet = Closet.objects.filter(Name=new_number)
            if len(old_closet) < 1:
                new_closet = Closet(Name=new_number, Old_Name=closet, School=school)
                new_closet.save()
            else:
                while len(old_closet) > 1:
                    old_closet[0].delete()
                new_closet = old_closet[0]
                new_closet.Old_Name = closet
                new_closet.School = school
                new_closet.save()
            vcnt=0
            for panel in panels:
                old_panel = Panel.objects.filter(Name=panel)
                if len(old_panel) < 1:
                    new_panel = Panel(Name=panel, School=school, Closet=new_closet, Voltage=voltages[vcnt])
                    new_panel.save()
                else:
                    while len(old_panel) > 1:
                        old_panel[0].delete()
                    new_panel = old_panel[0]
                    new_panel.School = school
                    new_panel.Closet = new_closet
                    new_panel.Voltage = voltages[vcnt]
                vcnt += 1
        else:
            vcnt = 0
            for panel in panels:
                old_panel = Panel.objects.filter(Name=panel)
                if len(old_panel) < 1:
                    new_panel = Panel(Name=panel, School=school, Voltage=voltages[vcnt])
                    new_panel.save()
                else:
                    while len(old_panel) > 1:
                        old_panel[0].delete()
                    new_panel = old_panel[0]
                    new_panel.School = school
                    new_panel.Voltage = voltages[vcnt]
                vcnt += 1
    df = pd.read_csv(file)
    df.fillna('')
    df.index = df['Panel']
    for panel in df.index:
        panel_obj = Panel.objects.get(Name=panel)
        parent_panel = Panel.objects.filter(Name=df['Parent Panel'][panel])
        if len(parent_panel) >= 1:
            parent_panel = parent_panel[0]
            panel_obj.Panels = parent_panel
            panel_obj.save()

"""

