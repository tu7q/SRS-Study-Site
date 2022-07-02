from django.conf import settings
import msal

ms_settings = settings.MICROSOFT_APP_SETTINGS

def get_user(token) -> :
    r = requests.get(
        url='{0}/me'.format(graph_url),
        headers={'Authorization': 'Bearer {0}'.format(token)}
    )
    return r.json()

def load_cache(request) -> :
    pass

def save_cache(request) -> :
    pass

def get_msal_app(cache=None) -> :
    pass

def get_sign_in_flow() -> :
    pass

def get_token_from_code(request) -> :
    pass

def get_token(request) -> :
    pass

def remove_user_and_token(request) -> :
    pass

def get_logout_url() -> :
    pass
