from django import forms
import pandas as pd
from ea_parser.script.file_transfer import _temporary_output_file_path

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

