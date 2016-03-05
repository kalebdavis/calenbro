from django.conf.urls import url
from django.contrib import admin
from myapp import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^event/new/', views.newEvent),
    url(r'^event/create/', views.createNewEvent),
    url(r'^event/(?P<eventID>[^/]+)', views.eventDetails)
]
