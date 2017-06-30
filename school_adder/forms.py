from django import forms
from energize_andover.models import *
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['Name']




class ClosetForm(forms.ModelForm):
    class Meta:
        model = Closet
        fields = ['Name', 'School']

class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['Name', 'Voltage', 'Location', 'Panels', 'School', 'Closet']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['Name', 'OldName', 'Type', 'School', 'Panels']
        widgets = {'Panels': forms.CheckboxSelectMultiple}

class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = ['Name', 'Number', 'Panel', 'Rooms']
        widgets = {'Rooms': forms.CheckboxSelectMultiple}

class AdderTypeForm(forms.Form):
    type = forms.ChoiceField(
        label='selcet object type to add',
        choices=[('', ''),
                 ('closet', 'closet'),
                 ('school', 'school'),
                 ('panel', 'panel'),
                 ('room', 'room'),
                 ('circuit', 'circuit'),
                 ],
        required=True
    )

def get_all_users():
    users = []
    usrs = User.objects.all()
    for i in usrs:
        users.append((i.username, i.username))
    return users

class PopulationForm(forms.Form):
    """
    School = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label='Existing School: ',
        required=True,
    )
    """
    New_School = forms.CharField(
        label='New School: ',
        required=True
    )

    Room_File = forms.FileField(
        label='Select a file for Room Mapping'
    )

    Panel_File = forms.FileField(
        label='Select a file for Panel and Circuit Mapping'
    )

    Device_File = forms.FileField(
        label='Select a file for Device Mapping'
    )

    all_users = forms.MultipleChoiceField(choices=get_all_users(),
                                          widget=forms.CheckboxSelectMultiple(),
                                          label="Which Users Can Access: ")

