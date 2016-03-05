from django.http import HttpResponse

def newEvent(request):
  return HttpResponse("Make a new event here.")

def eventDetails(request):
  return HttpResponse("Event details here")
