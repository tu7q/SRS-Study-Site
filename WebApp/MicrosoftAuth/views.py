from django.shortcuts import render, redirect

from .authentication import authenticate, BACKEND, BACKEND_PATH
from django.contrib.auth import login, logout
from django.conf import settings


def Login(request):
    auth_uri = BACKEND.setup(request)
    return render(request, "login.html", context={"auth_uri": auth_uri})


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
