from django.shortcuts import redirect, render
from django.http import HttpResponse
from MicrosoftAuthentication.decorators import RequireMSAuthentication

# Create your views here.


@RequireMSAuthentication
def Question(request, idx=0):
    return HttpResponse(f"Hello There! {request.session.get('user')}")
