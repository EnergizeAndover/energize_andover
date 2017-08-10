from django import forms
from energize_andover.models import *

class PanelEditForm(forms.Form):
    Name = forms.CharField(label = "Name: ")
