from django import forms

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
        label='Select a file'
    )

    graph = forms.BooleanField(
        label='Graph',
        required=False
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

    total_graph = forms.BooleanField(
        label="Is the data a running total:",
        required=False,
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


    total_graph = forms.BooleanField(
        label="Is the data a running total?:",
        required = False,
    )