from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class GeneratedEmail(models.Model):
    description = models.CharField(max_length=200)
    email_prefix = models.CharField(max_length=30)
    user = models.OneToOneField(User, unique=True)
