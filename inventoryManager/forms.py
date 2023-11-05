from django import forms
from datetime import datetime
from django.forms import ModelForm

from inventoryManager.models import *

# Define the forms below
class DateInput(forms.DateInput):
    input_type = 'date'

class OrganizationForm(forms.Form):
    name = forms.CharField(label = "Organization name:", max_length=32)
    contact_name = forms.CharField(label = "POC Name:", max_length=128)
    contact_email = forms.CharField(label = "POC Email:", max_length=128)
    about = forms.CharField(label = "Description:", max_length=128, required=False)

class OrderForm(forms.Form):
    posted = forms.DateField(widget=DateInput)
    ordered = forms.DateField(widget=DateInput, required=False)
    completed = forms.DateField(widget=DateInput, required=False)

    title = forms.CharField(max_length = 200)
    description = forms.CharField(max_length = 200, required=False)