import logging

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render

from .authentication import authenticate
from .authentication import BACKEND
from .authentication import BACKEND_PATH


def Login(request):
    auth_uri = BACKEND.setup(request)
    return render(request, "MicrosoftAuth/login.html", context={"auth_uri": auth_uri})


def Callback(request):
    user = authenticate(request)
    if user:
        login(request, user, backend=BACKEND_PATH)
    # settings.INDEX -> EEK
    return redirect(settings.LOGIN_REDIRECT_URL)


def Logout(request):
    logout(request)
    # settings.INDEX -> EEK
    return redirect(settings.LOGIN_URL)
