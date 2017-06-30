from django import forms
from energize_andover.models import *

def get_all_schools():
    schools = []
    query = School.objects.all()
    for i in query:
        schools.append((i.Name, i.Name))
    return schools

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

    approved_schools = forms.MultipleChoiceField(choices=get_all_schools(),
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
