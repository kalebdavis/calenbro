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
  
  startDate, endDate = getStartAndEnd(data.pop('daterange')[0])
  newEvent = Event(name= data.pop("name"), startDate=startDate, endDate=endDate, uuid= eventID)
  newEvent.save()

  return redirect(newEvent)

def getStartAndEnd(daterange):
  dates = daterange.split(' - ')
  startTime = datetime.strptime(dates[0], "%m/%d/%Y")
  endTime = datetime.strptime(dates[1], "%m/%d/%Y")
  return startTime, endTime

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