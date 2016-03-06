from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from outlook.authhelper import get_signin_url, get_token_from_code, get_user_email_from_id_token
from outlook.outlookservice import get_my_events
from ics import Calendar, Event
from myapp.models import Event as myappEvent
from myapp.models import Calendar as myappCalendar

def home(request):
    redirect_uri = request.build_absolute_uri(reverse('outlook:gettoken'))
    sign_in_url = get_signin_url(redirect_uri)
    return HttpResponse('<a href="' + sign_in_url + '">Click here to sign in</a>')

def gettoken(request):
    auth_code = request.GET['code']
    redirect_uri = request.build_absolute_uri(reverse('outlook:gettoken'))
    token = get_token_from_code(auth_code, redirect_uri)
    access_token = token['access_token']

    user_email = get_user_email_from_id_token(token['id_token'])

    request.session['access_token'] = access_token
    request.session['user_email'] = user_email
    return HttpResponseRedirect(reverse('outlook:events'))

def events(request):
    access_token = request.session['access_token']
    user_email = 'kalebdavis346@outlook.com'
    eventID = request.session['curEventID']
    curEvent = myappEvent.objects.get(uuid=eventID)

    if not access_token:
        return HttpResponseRedirect('/')
    else:
        events = get_my_events(access_token, user_email)
        newCalendar = myappCalendar(username=user_email, contents=parseEvents(events['value'], curEvent), event=curEvent)
        newCalendar.save()
        return redirect(curEvent)

def parseEvents(events, curEvent):
    c = Calendar()
    for e in events:
        event = Event()
        event.name = e['Subject']
        event.begin = e['Start']['DateTime']
        event.end = e['End']['DateTime']
        if event.begin >= curEvent.startDate and event.end <= curEvent.endDate:
          c.events.append(event)
    return c
