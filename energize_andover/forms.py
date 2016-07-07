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

    parse_symbol = forms.CharField(
        label='Symbol to separate data types:',
        required = False
    )

    total_graph = forms.BooleanField(
        label="Is the data a running total:",
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