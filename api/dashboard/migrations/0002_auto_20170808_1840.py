# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-08 18:40
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generatedemail',
            old_name='user',
            new_name='owner',
        ),
    ]
