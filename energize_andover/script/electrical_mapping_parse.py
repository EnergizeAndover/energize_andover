import pandas as pd
import numpy as np
import os
from mysite.settings import BASE_DIR
from energize_andover.models import *


TEMPORARY_INPUT_FILENAME = 'electrical_map.txt'

def create_mapping(form_data):
    _save_input_file(form_data['Mapping_file'])
    parse(_temporary_input_file_path(),form_data['School'])



def _temporary_input_file_path():
    return os.path.join(BASE_DIR, TEMPORARY_INPUT_FILENAME)

def _save_input_file(temporary_file):
    """Save the uploaded file to disk so it can be handled"""
    with open(_temporary_input_file_path(), 'wb') as fout:
        for chunk in temporary_file.chunks():
            fout.write(chunk)

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



