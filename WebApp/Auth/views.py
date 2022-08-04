from django.shortcuts import render, redirect
from .authentication import authenticate, BACKEND, BACKEND_PATH
from django.contrib.auth import login, logout


def Login(request):
    auth_uri = BACKEND.setup(request)
    return render(request, "login.html", context={"auth_uri": auth_uri})


def Callback(request):
    user = authenticate(request)
    if user:
        login(request, user, backend=BACKEND_PATH)
    # settings.INDEX -> EEK
    return redirect("Index")


def Logout(request):
    logout(request)
    # settings.INDEX -> EEK
    return redirect("Index")
