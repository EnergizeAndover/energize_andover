from django import forms
from .models import *
import pandas as pd
from energize_andover.script.file_transfer import _temporary_output_file_path



class NewSchoolForm(forms.Form):
    Name = forms.CharField(required=True)



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

