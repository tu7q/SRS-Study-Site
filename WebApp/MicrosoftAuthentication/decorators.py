from functools import wraps
from django.http import HttpRequest, HttpResponse
from typing import Callable

from django.shortcuts import redirect, resolve_url
from . import utils


def RequireMSAuthentication(
    view: Callable[[HttpRequest], HttpResponse]
) -> Callable[[HttpRequest], HttpResponse]:
    @wraps(view)
    def _view(request: HttpRequest) -> HttpResponse:
        if utils.is_authenticated(request.session):
            return view(request)
        return redirect("MSLogin")

    return _view
