from django.http import HttpResponse
from django.shortcuts import render

def newEvent(request):
  return render(request, 'newEvent.html')

def createNewEvent(request):
  return HttpResponse("")

def eventDetails(request, eventID):
  # curEvent = Event.find(eventID)
  # associatedCalendars = Calendar.filter(eventID)
  # context  = {'event': curEvent, 'calendars': associatedCalendars}
  return render(request, 'eventDetails.html')
