from django.http import HttpResponse
from django.shortcuts import render
import uuid
import sys
from myapp.models import Event
from datetime import datetime

def newEvent(request):
  return render(request, 'newEvent.html')

def createNewEvent(request):
  eventID = uuid.uuid4()
  # On the off chance the key exists already, make a new one
  while (len(Event.objects.filter(uuid= eventID)) > 0):
    eventID = uuid.uuid4()

  data = request.POST.copy()

  newEvent = Event(name= data.pop("Name"), startDate= datetime.now(), endDate= datetime.now(), uuid= eventID)
  # newEvent = Event(name= data.pop("Name"), startDate= data.pop("startDate"), endDate= data.pop('endDate'), uuid= eventID)
  newEvent.save()
  return HttpResponse(newEvent.name)

def eventDetails(request, eventID):
  curEvent = Event.objects.filter(uuid= eventID)[0]
  print >>sys.stderr, curEvent.name
  # associatedCalendars = Calendar.filter(eventID)
  context  = {'event': curEvent}
  return render(request, 'eventDetails.html', context)
