from django.conf.urls import url
from django.contrib import admin
from Calenbro import controller

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^event/new/', controller.newEvent),
    url(r'^event/create/', controller.createNewEvent),
    url(r'^event/(?P<eventID>[^/]+)/addCalendar', controller.addCalendar),
    url(r'^event/(?P<eventID>[^/]+)', controller.eventDetails)
]
