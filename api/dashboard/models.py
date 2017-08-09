from django.db import models

VISIBLE='VISIBLE'
HIDDEN='HIDDEN'
DELETED='DELETED'
VISIBILITY_CHOICES = [(VISIBLE, 'Email is visible on the dashboard.'), 
                      (HIDDEN, 'Email is removed, but can be readded.'), 
                      (DELETED, 'Email is permanently deleted.')]


class GeneratedEmail(models.Model):
    description = models.CharField(max_length=200)
    email = models.CharField(max_length=50)
    forward = models.BooleanField(default=True)
    visibility = models.CharField(choices=VISIBILITY_CHOICES, max_length=20, default=VISIBLE)
    owner = models.ForeignKey('auth.User', related_name='emails', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']


