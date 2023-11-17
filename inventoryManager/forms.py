from django import forms
from datetime import datetime
from django.forms import ModelForm

from inventoryManager.models import *

# Define the forms below
class DateInput(forms.DateInput):
    input_type = 'date'

class OrganizationForm(forms.Form):
    name = forms.CharField(label = "Organization name:", max_length=32)
    about = forms.CharField(label = "Description:", max_length=128, required=False)

class OrderForm(forms.Form):
    posted = forms.DateField(widget=DateInput)
    ordered = forms.DateField(widget=DateInput, required=False)
    completed = forms.DateField(widget=DateInput, required=False)

    title = forms.CharField(max_length = 200)
    description = forms.CharField(max_length = 200, required=False)

class UserCreateForm(forms.Form):
    username = forms.CharField(max_length = 200)
    password = forms.CharField(max_length = 200)
    email = forms.CharField(max_length = 200)
    first_name = forms.CharField(max_length = 200)
    last_name = forms.CharField(max_length = 200)

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length = 200)
    password = forms.CharField(max_length = 200)

class UserChangePasswordForm(forms.Form):
    oldPassword = forms.CharField(max_length = 200)
    password = forms.CharField(max_length = 200)

class OrderItemForm(forms.Form):
    itemName = forms.CharField(max_length = 200)
    itemNsn = forms.CharField(max_length = 200)
    itemQuantity = forms.DecimalField(max_digits=5, decimal_places=0)
    itemCost = forms.DecimalField(max_digits=12, decimal_places=2)