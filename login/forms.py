from django.forms import EmailField, forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"]
        if "@nospammail.org" in email:
            raise forms.ValidationError("You cannot register using a nospammail address!")
        return email

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        if commit:
            user.save()
        return user