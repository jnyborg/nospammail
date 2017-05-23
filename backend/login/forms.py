from django.forms import EmailField, forms
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserCreationForm(UserCreationForm):
    email = EmailField(label=_("Email address"), required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def clean(self):
        cleaned_data = super(UserCreationForm, self).clean()

        if cleaned_data.get("email"):
            email = cleaned_data["email"]

            if "@nospammail.org" in email:
                raise ValidationError("You cannot register using a nospammail address.")
            elif User.objects.filter(email=email).exists():
                raise forms.ValidationError("A user with that email address already exists.")
            return cleaned_data

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)

        if commit:
            user.save()
        return user