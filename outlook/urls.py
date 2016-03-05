from django.conf.urls import patterns, url
from outlook import views

urlpatterns = patterns('',
    url(r'^$', views.home, name='home'),
    url(r'^home/$', views.home, name='home'),
    url(r'^gettoken/$', views.gettoken, name='gettoken'),
    url(r'^events/$', views.events, name='events'),
)
