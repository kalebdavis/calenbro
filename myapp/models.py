from __future__ import unicode_literals

from django.db import models
import ics
import sys

class Event(models.Model):
    name = models.CharField(max_length=140)
    startDate = models.DateTimeField()
    endDate = models.DateTimeField()
    uuid = models.CharField(max_length=50)
    ownerName = models.CharField(max_length=60)
    ownerEmail = models.EmailField(max_length=254)

    def __str__(self):
      return str(name)

    def get_absolute_url(self):
        return "/event/" + str(self.uuid)

class Calendar(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.CharField(max_length=100)
    contents = models.TextField()

    def getCalendar(self):
        return ics.Calendar(contents.decode('iso-8859-1'))

    def getEventList(self):
        c = getCalendar()
        return c.events

    def parseCalendar(icsFile):
        return ics.Calendar(icsFile)

