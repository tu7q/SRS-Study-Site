from django.contrib.sessions.backends.base import SessionBase
from typing import Any, Dict, Optional
from django.http import HttpRequest
from . import settings as s 
import requests
import msal


def load_cache(session: SessionBase) -> msal.SerializableTokenCache:
    cache = msal.SerializableTokenCache()
    # check for token cache in session
    if (session.get(s.TOKEN_CACHE)):
        cache.deserialize(session[s.TOKEN_CACHE])
    return cache

def save_cache(session: SessionBase, cache: msal.SerializableTokenCache) -> None:
    # If cache has changes persist it in the session
    if cache.has_state_changed:
        session[s.TOKEN_CACHE] = cache.serialize()

def clear_cache(session: SessionBase) -> None:
    if (session.get(s.TOKEN_CACHE)):
        session.pop(s.TOKEN_CACHE)
    if (session.get('user')):
        session.pop('user')
    # clear other session data

def get_msal_app(cache: msal.SerializableTokenCache=None) -> msal.ConfidentialClientApplication:
    # intialize msal client
    auth_app = msal.ConfidentialClientApplication(
        s.APP_ID,
        authority=s.AUTHORITY,
        client_credential=s.APP_SECRET,
        token_cache=cache
    )
    return auth_app

def get_sign_in_flow() -> Dict[str, Any]: # I think thats the return type
    auth_app = get_msal_app()
    return auth_app.initiate_auth_code_flow(
        s.SCOPES#,
        #redirect_url=s.REDIRECT
    )

def get_token_from_code(request: HttpRequest) -> Optional[str]: # close enough
    cache = load_cache(request.session)
    auth_app = get_msal_app(cache)
    flow = request.session.pop('auth_flow', {})
    try:
        result = auth_app.acquire_token_by_auth_code_flow(
            flow, 
            request.GET
        )
        if 'error' in result:
            print(result)
            print("\nERROR IN RESULTs\n")
            return None # something went wrong
    except ValueError: # usually caused by CSRF
        print("\nVALUE ERORr\n")
        return None
    save_cache(request.session, cache)
    #print('token result: ', result)
    return result.get('access_token', None)

def get_user(token: str) -> Dict[str, str]: # Should be accurate enough 
    r = requests.get(
        url=f'{s.GRAPH_URL}/me',
        headers={f'Authorization': 'Bearer {token}'}
    )
    print('status code: ', r.status_code)
    if r.status_code == requests.status_codes.codes.ok:
        return r.json()
    return {} # empty lmao

def store_user(session: SessionBase, user: Dict[str, str]) -> None: # close enough
    print('user: ', user)
    session['user'] = {
        'is_authenticated': True,
        'name': user.get('displayName', ''),
        'email': user.get('mail', '')
    }

# is this needed??? 
def get_logout_url() -> None:
    pass

def is_authenticated(session: SessionBase) -> bool:
    user = session.get('user', {})
    if user.get('is_authenticated', False):
        return True
    return False
