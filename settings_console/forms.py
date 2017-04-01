from django import forms
from django.forms import EmailField
from settings_console.models import GeneratedEmail

class ToggleEmailsForm(forms.Form):
    id = forms.IntegerField()


