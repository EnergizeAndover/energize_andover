from django import forms
from energize_andover.models import *
class SchoolForm(forms.ModelForm):
    class Meta:
        model = School
        fields = ['Name']



class ClosetForm(forms.ModelForm):
    class Meta:
        model = Closet
        fields = ['Name', 'Old_Name']

class PanelForm(forms.ModelForm):
    class Meta:
        model = Panel
        fields = ['Name', 'Voltage']


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['Name', 'OldName', 'Type']

class CircuitForm(forms.ModelForm):
    class Meta:
        model = Circuit
        fields = ['Name', 'Number', 'Panel']
        #widgets = {'Rooms': forms.CheckboxSelectMultiple, 'Devices': forms.CheckboxSelectMultiple}

class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ['Name']

class AdderTypeForm(forms.Form):
    type = forms.ChoiceField(
        label='Select object type to add',
        choices=[('', ''),
                 ('Closet', 'Closet'),
                 #('School', 'School'),
                 ('Panel', 'Panel'),
                 ('Room', 'Room'),
                 ('Device', 'Device')
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

    Device_Association_File = forms.FileField(
        label='Select a file for Additional Device Info',
        required = False
    )

    all_users = forms.MultipleChoiceField(choices=get_all_users(),
                                          widget=forms.CheckboxSelectMultiple(),
                                          label="Which Users Can Access: ")


