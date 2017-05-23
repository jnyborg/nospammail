from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm


# Create your models here.
class GeneratedEmail(models.Model):
    description = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    enabled = models.BooleanField(default=True)
    hidden = models.BooleanField(default=False)
    deleted= models.BooleanField(default=False)
    class Meta:
        ordering = ['-id']


class GeneratedEmailForm(ModelForm):
    class Meta:
        model = GeneratedEmail
        fields = ["description", "email"]

