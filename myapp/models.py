from __future__ import unicode_literals

from django.db import models
import ics

class Event(models.Model):
    name = models.CharField(max_length=140)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()

class Calendar(models.Model):
    event = models.ForeignKey(Event)
    username = models.CharField(max_length=100)
    contents = models.TextField()

    def getCalendar(self):
        return ics.Calendar(contents.decode('iso-8859-1'))
