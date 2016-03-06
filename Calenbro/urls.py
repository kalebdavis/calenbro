from django.conf.urls import url, patterns, include
from django.contrib import admin
from myapp import views as myappviews
from outlook import views as outlookviews
from . import controller

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^event/new/', controller.newEvent),
    url(r'^event/create/', controller.createNewEvent),
    url(r'^event/(?P<eventID>[^/]+)/addCalendar', controller.addCalendar),
    url(r'^$', outlookviews.home, name='home'),
    url(r'^outlook/', include('outlook.urls', namespace='outlook')),
    url(r'^event/(?P<eventID>[^/]+)/$', controller.eventDetails)
]
