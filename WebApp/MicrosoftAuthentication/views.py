from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.conf import settings
import requests
from . import utils

from MicrosoftAuthentication.utils import get_logout_url, get_sign_in_flow

# global constants are acceptable
LoginCallback = settings.MICROSOFT_APP_SETTINGS.get('redirect', None)
assert LoginCallback is not None, "Microsoft Redirect was None."

def Login(request):
    flow = get_sign_in_flow()
    request.session['auth_flow'] = flow
    return redirect(flow['auth_uri'])

def Logout(request):
    # django logout(request)
    return HttpResponseRedirect(get_logout_url())

def Callback(request):
    result = get_token_from_code(request)
    ms_user = get_user(result['access_token'])
    user = get_django_user(email=ms_user['mail'])
    if user:
        #django login(request, user)
        pass
    else:
        return HttpResponseForbidden("INVALID YOU FOOL!")
    return redirect(settings.LOGIN_REDIRECT_URL)
