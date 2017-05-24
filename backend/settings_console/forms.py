from django import forms

class ToggleEmailsForm(forms.Form):
    id = forms.IntegerField()