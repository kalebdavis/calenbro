from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.shortcuts import redirect
import ics
import uuid
import sys
from myapp.models import Event
from myapp.models import Calendar
from outlook.authhelper import get_signin_url
from datetime import datetime, date
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

  # get data for heat map
  heapData = createDataFromHeap(createHeapMap(request, eventID))
  context  = {'event': curEvent, 'calendars': associatedCalendars, 'signin_url': sign_in_url, 'heapData': heapData }

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
  print(createDataFromHeap(heap))
  return heap

def createDataFromHeap(heap):
  mapOfDates = {
                date(2016,3,1): [2,4],
                date(2016,3,2): [3,4],
                date(2016,3,3): [4,4],
                date(2016,3,4): [5,4],
                date(2016,3,5): [6,4],
                date(2016,3,6): [0,3],
                date(2016,3,7): [1,3],
                date(2016,3,8): [2,3],
                date(2016,3,9): [3,3],
                date(2016,3,10): [4,3],
                date(2016,3,11): [5,3],
                date(2016,3,12): [6,3],
                date(2016,3,13): [0,2],
                date(2016,3,14): [1,2],
                date(2016,3,15): [2,2],
                date(2016,3,16): [3,2],
                date(2016,3,17): [4,2],
                date(2016,3,18): [5,2],
                date(2016,3,19): [6,2],
                date(2016,3,20): [0,1],
                date(2016,3,21): [1,1],
                date(2016,3,22): [2,1],
                date(2016,3,23): [3,1],
                date(2016,3,24): [4,1],
                date(2016,3,25): [5,1],
                date(2016,3,26): [6,1],
                date(2016,3,27): [0,0],
                date(2016,3,28): [1,0],
                date(2016,3,29): [2,0],
                date(2016,3,30): [3,0],
                date(2016,3,31): [4,0],
               }
  data = []
  for k,v in mapOfDates.iteritems():
    if k in heap.keys():
      d = v
      d.append(heap[k])
      data.append(d)
    else:
      d = v
      d.append(0)
      data.append(d)
  return data
