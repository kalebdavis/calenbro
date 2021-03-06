# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-06 06:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_event_uuid'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='ownerEmail',
            field=models.EmailField(default='kaleb.davis39@gmail.com', max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='ownerName',
            field=models.CharField(default='Kaleb Davis', max_length=60),
            preserve_default=False,
        ),
    ]
