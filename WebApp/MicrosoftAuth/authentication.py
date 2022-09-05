from django.views.decorators.debug import sensitive_variables
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.conf import settings

from MicrosoftAuth.backends import MicrosoftAuthentication
from django.contrib import auth

BACKEND_PATH = "MicrosoftAuth.backends.MicrosoftAuthentication"
BACKEND = MicrosoftAuthentication()

if BACKEND_PATH not in settings.AUTHENTICATION_BACKENDS:
    raise Exception(f"BACKEND: {BACKEND.__class__.__name__} not in authentication backends")


@sensitive_variables("credentials")
def authenticate(request, **credentials):
    """
    A replacement to the default Django authenticate method to allow authentication using the Microsoft Auth backend.
    If the given credentials are valid, return a User object.
    """
    try:
        user = BACKEND.authenticate(request)  # , **credentials)
    except PermissionDenied:
        return
    if user is not None:
        user.backend = BACKEND_PATH
        return user
