from urllib.robotparser import RequestRate
from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse
from MicrosoftAuthentication.decorators import RequireMSAuthentication

# List of possible subjects
@RequireMSAuthentication
def Index(request: HttpRequest) -> HttpResponse:
    pass


@RequireMSAuthentication
def Question(request: HttpRequest, idx=0) -> HttpResponse:
    return HttpResponse(f"Hello There! {request.session.get('user')}")
