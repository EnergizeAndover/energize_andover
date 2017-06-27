from django import forms
from energize_andover.models import *

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