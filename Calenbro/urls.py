from django.conf.urls import url, patterns, include
from django.contrib import admin
from outlook import views as outlookviews
from . import controller
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^event/$', controller.allEvents),
    url(r'^event/new/', controller.newEvent),
    url(r'^event/create/', controller.createNewEvent),
    url(r'^event/(?P<eventID>[^/]+)/$', controller.eventDetails),
    url(r'^event/(?P<eventID>[^/]+)/addCalendar', controller.addCalendar),
    url(r'^$', controller.home, name='home'),
    url(r'^outlook/', include('outlook.urls', namespace='outlook')),
]

urlpatterns += staticfiles_urlpatterns()
