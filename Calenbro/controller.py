from django.shortcuts import render
from django.shortcuts import redirect
import uuid
import sys
from myapp.models import Event
from myapp.models import Calendar
from datetime import datetime

def newEvent(request):
  return render(request, 'newEvent.html')

def createNewEvent(request):
  eventID = uuid.uuid4()
  # On the off chance the key exists already, make a new one
  while (len(Event.objects.filter(uuid= eventID)) > 0):
    eventID = uuid.uuid4()
  data = request.POST.copy()

  newEvent = Event(name= data.pop("name"), startDate= datetime.now(), endDate= datetime.now(), uuid= eventID)
  newEvent.save()

  return redirect(newEvent)

def eventDetails(request, eventID):
  curEvent = Event.objects.filter(uuid= eventID)[0]
  associatedCalendars = Calendar.objects.filter(event= curEvent)
  context  = {'event': curEvent, 'calendars': associatedCalendars}
  return render(request, 'eventDetails.html', context)

def addCalendar(request, eventID):
  curEvent = Event.objects.filter(uuid= eventID)[0]
  requestData = request.POST.copy()
  uploadedFile = request.FILES['contents']
  parsedCalendar = uploadedFile.read()

  newCalendar = Calendar(username= requestData.pop("name"), contents= parsedCalendar, event= curEvent)
  newCalendar.save()

  return redirect(curEvent)
