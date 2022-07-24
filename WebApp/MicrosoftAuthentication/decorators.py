# WebApp/MicrosoftAuthentication/decorators.py

from functools import wraps
from django.http import HttpRequest, HttpResponse
from typing import Callable

from django.shortcuts import redirect, resolve_url
from . import utils


def RequireMSAuthentication(view: Callable[[HttpRequest], HttpResponse]) -> Callable[[HttpRequest], HttpResponse]:
    """Support for type hinting a decorated function is unclear. This SO answer might be helpful: https://stackoverflow.com/a/68290080"""

    @wraps(view)
    def _view(request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if utils.is_authenticated(request.session):
            return view(request, *args, **kwargs)
        return redirect("MSLogin")

    return _view
