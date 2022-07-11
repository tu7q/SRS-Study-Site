from django.shortcuts import redirect, render
from django.http import (
    HttpRequest,
    HttpResponse,
    HttpResponseForbidden,
    HttpResponseRedirect,
)
from . import settings as s
from . import utils


def Login(request: HttpRequest) -> HttpResponse:
    if utils.is_authenticated(request.session):
        return redirect(s.INDEX_REDIRECT)
    flow = utils.get_sign_in_flow()
    request.session["auth_flow"] = flow
    return render(
        request,
        "MicrosoftAuthentication/login.html",
        context={"auth_uri": flow["auth_uri"]},
    )


def Logout(request: HttpRequest) -> HttpResponse:
    # django logout(request)
    # return HttpResponseRedirect(get_logout_url())
    utils.clear_cache(request.session)
    return redirect(utils.logout_url())


def Callback(request: HttpRequest) -> HttpResponse:
    token = utils.get_token_from_code(request)
    ms_user = utils.get_user(token)
    if ms_user is None:
        return redirect("error")
    utils.store_user(request.session, ms_user)
    return redirect(s.INDEX_REDIRECT)
