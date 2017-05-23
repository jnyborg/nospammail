from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.core.validators import MinValueValidator, MaxValueValidator

from enum import IntEnum

class EmailVisiblity(IntEnum):
    VISIBLE = 0
    HIDDEN = 1
    DELETED = 2

# Create your models here.
class GeneratedEmail(models.Model):
    description = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    user = models.ForeignKey(User)
    enabled = models.BooleanField(default=True)
    visibility = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(8)])
    class Meta:
        ordering = ['-id']


class GeneratedEmailForm(ModelForm):
    class Meta:
        model = GeneratedEmail
        fields = ["description", "email"]