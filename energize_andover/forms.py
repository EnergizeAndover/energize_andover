from django import forms
from .models import *
import pandas as pd
from energize_andover.script.file_transfer import _temporary_output_file_path


class MetasysUploadForm(forms.Form):
    summarize = forms.BooleanField(
        label='Group by day',
        required=False
    )

    cost = forms.FloatField(
        label='Estimated cost of electricity ($/kWh)',
        required=False
    )

    start_time = forms.TimeField(
        label='Start time (HH:MM)',
        input_formats=['%H:%M'],
        required=False
    )

    end_time = forms.TimeField(
        label='End time (HH:MM)',
        input_formats=['%H:%M'],
        required=False
    )

    metasys_file = forms.FileField(
        label='Select a file to parse'
    )

    columns_file = forms.FileField(
        label='Select a file for column headers',
        required=False,
    )

    graph = forms.BooleanField(
        label='Graph',
        required=False
    )


class GraphUploadForm(forms.Form):
    parsed_file = forms.FileField(
        label='Select a Metasys file',
        required=True,

    )

    graph_period = forms.ChoiceField(
        label='Time Interval:',
        choices=[('min', 'all data'),
                 ('hour', 'hour'),
                 ('day', 'day'),
                 ('month', 'month'),
                 ],
        required=False,
    )

    graph_data = forms.CharField(
        label='Data to graph:',
        required=False,
    )

    parse_symbol = forms.CharField(
        label='Symbol to separate data types:',
        required=False
    )

    total_graph = forms.BooleanField(
        label="Is the data a running total?:",
        required=False,
    )

    multiplot = forms.BooleanField(
        label='Plot on one graph:',
        required=False
    )

    y_axis_label = forms.CharField(
        label="Enter title of Y-axis",
        required=False,
    )

    graph_title = forms.CharField(
        label="Enter title of graph",
        required=False,
    )

    graph_type = forms.ChoiceField(
        label='select graph type:',
        choices=[('line', 'line plot'),
                 ('bar', 'vertical bar plot'),
                 ('barh', 'horizontal bar plot'),
                 ('area', 'area plot'),
                 ]
    )

class SmartGraphUploadForm(forms.Form):


    graph_period = forms.ChoiceField(
        label='Time Interval:',
        choices=[('min', 'all data'),
                 ('hour', 'hour'),
                 ('day', 'day'),
                 ('month', 'month'),
                 ],
        required=False,
    )

    graph_data = forms.MultipleChoiceField(
        label='Data to graph:',
        choices=[(choice, choice)for choice in pd.read_csv(_temporary_output_file_path(), header=1, index_col=[0]).columns],
        required=True,
        widget=forms.CheckboxSelectMultiple,
    )

    parse_symbol = forms.CharField(
        label='Symbol to separate data types:',
        required=False
    )

    total_graph = forms.BooleanField(
        label="Is the data a running total?:",
        required=False,
    )

    multiplot = forms.BooleanField(
        label='Plot on one graph:',
        required=False
    )

    y_axis_label = forms.CharField(
        label="Enter title of Y-axis",
        required=False,
    )

    graph_title = forms.CharField(
        label="Enter title of graph",
        required=False,
    )

    graph_type = forms.ChoiceField(
        label='select graph type:',
        choices=[('line', 'line plot'),
                 ('bar', 'vertical bar plot'),
                 ('barh', 'horizontal bar plot'),
                 ('area', 'area plot'),
                 ]
    )

    def __init__(self, *args, **kwargs):
        super(SmartGraphUploadForm, self).__init__(*args, **kwargs)
        self.fields['graph_data'].choices = [(choice, choice) for choice in
                                             pd.read_csv(_temporary_output_file_path(), header=1,
                                                         index_col=[0]).columns]


class NewSchoolForm(forms.Form):
    Name = forms.CharField(required=True)


class SchoolForm(forms.ModelForm):
    users = []
    usrs = User.objects.all()
    for i in usrs:
        users.append((i.username, i.username))
    all_users = forms.MultipleChoiceField(choices=users,
                                          widget=forms.CheckboxSelectMultiple(),
                                          label="Which Users Can Access: ")
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

class PopulationForm(forms.Form):
    School = forms.ModelChoiceField(
        queryset=School.objects.all(),
        label='School: ',
        required=True,
    )

    Mapping_file = forms.FileField(
        label='Select a file to Map from'
    )

class SearchForm(forms.Form):
    entry = forms.CharField(
        label = 'Search:',
        required = False
    )
    school = forms.CharField(
        required = False
    )
    rooms = forms.BooleanField(
        label = 'Rooms',
        required = False
    )
    panels = forms.BooleanField(
        label = 'Panels',
        required = False
    )
    circuits = forms.BooleanField(
        label = 'Devices',
        required = False
    )
    closets = forms.BooleanField(
        label = 'Closets',
        required = False
    )

class LoginForm(forms.Form):
    username = forms.CharField(
        label = 'Username: ',
        required = True
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label = "Password: ",
        required=True
    )

class NewUserForm(forms.Form):
    username = forms.CharField(
        label='Username: ',
        required=True
    )
    email = forms.EmailField(
        label="Email: ",
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label="Password: ",
        required=True
    )
    schools = []
    query= School.objects.all()
    for i in query:
        schools.append((i.Name, i.Name))
    approved_schools = forms.MultipleChoiceField(choices=schools,
                                                 widget=forms.CheckboxSelectMultiple(),
                                                 label = "Approved Schools")
    master_username = forms.CharField(
        label = "Administrator Username: ",
        required = True
    )
    master_password = forms.CharField(
        widget=forms.PasswordInput,
        label="Administrator Password: ",
        required=True
    )
