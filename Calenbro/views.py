from django.http import HttpResponse

def newEvent(request):
  return HttpResponse("Make a new event here.")

def createNewEvent(request):
  return HttpResponse("")

def eventDetails(request, eventID):
  return HttpResponse("Getting event data for " + eventID)
