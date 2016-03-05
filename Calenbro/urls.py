from django.conf.urls import url, patterns, include
from django.contrib import admin
from myapp import views as myappviews
from outlook import views as outlookviews

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^event/new/', myappviews.newEvent),
    url(r'^event/create/', myappviews.createNewEvent),
    url(r'^event/(?P<eventID>[^/]+)', myappviews.eventDetails),
    url(r'^$', outlookviews.home, name='home'),
    url(r'^outlook/', include('outlook.urls', namespace='outlook')),
]
