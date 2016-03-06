from urlparse import urlparse
from urllib import urlencode
import requests
import base64
import json

# Client ID and secret
client_id = '13d03612-0baa-4380-b52f-5abc76213073'
client_secret = 'dMW51APMFh28FOuQS2hSG9H'

# Constant strings for Oauth2 flow
authority = 'https://login.microsoftonline.com'

# Authorize URL that initiates the OAuth2 client credential flow for admin consent
authorize_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/authorize?{0}')

# Token issuing endpoint
token_url = '{0}{1}'.format(authority, '/common/oauth2/v2.0/token')

# Scopes required by the app
scopes = [ 'openid',
           'https://outlook.office.com/mail.read',
           'https://outlook.office.com/calendars.read',
         ]

def get_signin_url(redirect_uri):
    params = {
              'client_id': client_id,
              'redirect_uri': redirect_uri,
              'response_type': 'code',
              'scope': ' '.join(str(i) for i in scopes)
              }
    signin_url = authorize_url.format(urlencode(params))

    return signin_url

def get_token_from_code(auth_code, redirect_uri):
    post_data = {
                  'grant_type': 'authorization_code',
                  'code': auth_code,
                  'redirect_uri': redirect_uri,
                  'scope': ' '.join(str(i) for i in scopes),
                  'client_id': client_id,
                  'client_secret': client_secret
                }
    r = requests.post(token_url, data = post_data)
    try:
        return r.json()
    except:
        return 'Error retrieving token: {0} - {1}'.format(r.status_code, r.text)

def get_user_email_from_id_token(id_token):
    token_parts = id_token.split('.')
    encoded_token = token_parts[1]

    leftovers = len(encoded_token) % 4
    if leftovers == 2:
        encoded_token += '=='
    elif leftovers == 3:
        encoded_token += '='

    decoded = base64.urlsafe_b64decode(encoded_token.encode('utf-8')).decode('utf-8')

    jwt = json.loads(decoded)

    return jwt
