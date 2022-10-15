from typing import Any
from typing import Optional

import msal
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.http import HttpRequest
from get_docker_secret import get_docker_secret


UserModel = get_user_model()

# ms app settings
HOST = "https://ncea-srs.duckdns.org"

APP_ID = get_docker_secret("ms_app_id")
APP_SECRET = get_docker_secret("ms_secret")
REDIRECT = HOST + "/auth/callback/"
SCOPES = ["https://graph.microsoft.com/user.read"]
AUTHORITY = "https://login.microsoftonline.com/organizations"

LOGOUT_URL = AUTHORITY + "/oauth2/v2.0/logout"  # should this be URI?

# MS graph url
GRAPH_URL = "https://graph.microsoft.com/v1.0"  # whatever it was


class MicrosoftAuthentication(BaseBackend):
    SESSION_KEY = "MICROSOFT"
    AUTH = "MICROSOFT"

    def setup(self, request) -> str:
        app = self._get_confidential_app()
        flow = app.initiate_auth_code_flow(SCOPES, max_age=10 * 60, redirect_uri=REDIRECT)
        self.to_store(request, flow)
        return flow["auth_uri"]

    def authenticate(self, request):
        flow = self.from_store(request)
        if not flow:
            return
        app = self._get_confidential_app()
        try:
            token = app.acquire_token_by_auth_code_flow(flow, request.GET)
        except ValueError:
            return
        if "error" in token:
            return
        ms_user = self._get_user(token)
        if not ms_user:
            return
        user, created = UserModel._default_manager.get_or_create(**ms_user)
        if self.user_can_authenticate(user):
            return user

    def get_user(self, user_pk):
        try:
            user = UserModel._default_manager.get(pk=user_pk)
        except UserModel.DoesNotExist:
            return None
        if self.user_can_authenticate(user):
            return user
        # return user if self.user_can_authenticate(user) else None

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, "is_active", None)
        return is_active or is_active is None

    @classmethod
    def _get_confidential_app(cls):
        return msal.ConfidentialClientApplication(APP_ID, authority=AUTHORITY, client_credential=APP_SECRET)

    def to_store(self, request: HttpRequest, data: Any) -> None:
        request.session[self.SESSION_KEY] = data

    def from_store(self, request: HttpRequest) -> Optional[Any]:
        return request.session.get(self.SESSION_KEY)

    @classmethod
    def _get_user(cls, token):
        access_token = token.get("access_token", "")
        r = requests.get(url=f"{GRAPH_URL}/me", headers={"Authorization": f"Bearer {access_token}"})
        if r.status_code == requests.status_codes.codes.ok:
            user = r.json()
            return {
                "email": user["mail"],  # must contain mail field
                "name": user.get("displayName", ""),  # displayName is optional
            }
        return None
