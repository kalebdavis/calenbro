import requests
import uuid
import json

outlook_api_endpoint = 'https://outlook.office.com/api/v2.0{0}'

def make_api_call(method, url, token, user_email, payload=None, parameters=None):
    headers = {
                'User-Agent': 'brickhack/1.0',
                'Authorization': 'Bearer {0}'.format(token),
                'Accept': 'application/json',
                'X-AnchorMailbox': 'user_email'
                }

    request_id = str(uuid.uuid4())
    instrumentation = {
                        'client-request-id': request_id,
                        'return-client-request-id': 'true'
                      }

    headers.update(instrumentation)
    response = None

    if(method.upper() == 'GET'):
        response = requests.get(url, headers=headers, params=parameters)
    elif(method.upper() == 'DELETE'):
        response = requests.delete(url, headers=headers, params=parameters)
    elif(method.upper() == 'PATCH'):
        headers.update({ 'Content-Type': 'application/json' })
        response = requests.patch(url, headers=headers, data=json.dumps(payload), params=parameters)
    elif(method.upper() == 'POST'):
        headers.update({ 'Content-Type': 'application/json' })
        response = requests.post(url, headers=headers, data=json.dumps(payload), params=parameters)
    return response

def get_my_events(access_token, user_email):
    get_events_url = outlook_api_endpoint.format('/Me/Events')

    query_parameters = {
                        '$top': '10',
                        '$select': 'Subject,Start,End',
                        '$orderby': 'Start/DateTime ASC'
                       }
    r = make_api_call('GET', get_events_url, access_token, user_email, parameters=query_parameters)

    if(r.status_code == requests.codes.ok):
        return r.json()
    else:
        return "{0}: {1}".format(r.status_code, r.text)
