from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import redirect
import ics
import uuid
import sys
from myapp.models import Event
from myapp.models import Calendar
from outlook.authhelper import get_signin_url
from datetime import datetime
from ics import Calendar as ICSCalendar

def home(request):
  return render(request, 'home.html', {})

def allEvents(request):
  events = Event.objects.all()
  context = { 'events': events }
  return render(request, 'events.html', context)

def newEvent(request):
  return render(request, 'newEvent.html')

def createNewEvent(request):
  eventID = uuid.uuid4()
  # On the off chance the key exists already, make a new one
  while (len(Event.objects.filter(uuid= eventID)) > 0):
    eventID = uuid.uuid4()
  data = request.POST.copy()
  
  startDate, endDate = getStartAndEnd(data.pop('daterange')[0])
  newEvent = Event(name= data.pop("name")[0], startDate=startDate, endDate=endDate, uuid= eventID, ownerName=data.pop('ownerName')[0], ownerEmail=data.pop('ownerEmail')[0])
  newEvent.save()

  return redirect(newEvent)

def getStartAndEnd(daterange):
  dates = daterange.split(' - ')
  startTime = datetime.strptime(dates[0], "%m/%d/%Y")
  endTime = datetime.strptime(dates[1], "%m/%d/%Y")
  return startTime, endTime

def eventDetails(request, eventID):
  curEvent = Event.objects.get(uuid= eventID)
  associatedCalendars = Calendar.objects.filter(event= curEvent)
  redirect_uri = request.build_absolute_uri(reverse('outlook:gettoken'))
  sign_in_url = get_signin_url(redirect_uri)
  request.session['curEventID'] = eventID
  context  = {'event': curEvent, 'calendars': associatedCalendars, 'signin_url': sign_in_url }

  createHeapMap(request, eventID)
  return render(request, 'eventDetails.html', context)

def addCalendar(request, eventID):
  curEvent = Event.objects.get(uuid= eventID)
  minDate = curEvent.startDate
  maxDate = curEvent.endDate
  requestData = request.POST.copy()
  uploadedFile = request.FILES['contents']
  parsedCalendar = uploadedFile.read()

  cal = ICSCalendar(parsedCalendar)
  calendarEvents = cal.events
  calendarEvents[:] = [x for x in calendarEvents if not (x.begin < minDate or x.end > maxDate)]
  cal.events = calendarEvents

  newCalendar = Calendar(username= requestData.pop("name"), contents= str(cal), event= curEvent)
  newCalendar.save()

  return redirect(curEvent)

def createHeapMap(request, eventID):
  curEvent = Event.objects.get(uuid=eventID)
  calendars = Calendar.objects.filter(event=curEvent)
  minDate = curEvent.startDate.date()
  maxDate = curEvent.endDate.date()

  heap = {}
  for c in calendars:
    c = ICSCalendar(c.contents)
    for e in c.events:
      startDate = e.begin.date()
      endDate = e.end.date()
      if startDate >= minDate and endDate <= maxDate:
        if startDate not in heap:
          heap[startDate] = 1
        else:
          heap[startDate] += 1
  print(heap)
  return heap
