# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-23 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings_console', '0004_generatedemail_enabled'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generatedemail',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='generatedemail',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='generatedemail',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]