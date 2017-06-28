from django import forms
from energize_andover.models import *

class PanelEditForm(forms.Form):
    Name = forms.CharField(label = "Name: ")
    Voltage = forms.CharField(label="Voltage: ")
    Notes = forms.CharField(label="Notes: ")
    clos = []
    closets = Closet.objects.all()
    for i in closets:
        clos.append((i.Name, i.Name))
    Closet = forms.MultipleChoiceField(choices=clos,
                                       label="Closet Where Panel is Found: ")
    rooms = []
    allrooms = Room.objects.all()
    for i in allrooms:
        rooms.append((i.Name, i.Name))
    Rooms = forms.MultipleChoiceField(choices=rooms,
                                      widget=forms.SelectMultiple(),
                                      label = "Associated Rooms: ")

    pans = []
    panels = Panel.objects.all()
    for i in panels:
        pans.append((i.Name, i.Name))
    Parent = forms.MultipleChoiceField(choices = pans,
                                       widget=forms.SelectMultiple(),
                                       label = "Parent Panel: ")

