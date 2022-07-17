# WebApp/MicrosoftAuthentication/settings.py

# some important constants

HOST = "http://localhost:8000"

# ms app settings
APP_ID = "6db743c4-b783-4604-9808-799282822dcb"
APP_SECRET = "lST8Q~HZYeHUzm2b9JZ~1AsyHS9avPpkwSnSUaHU"
REDIRECT = HOST + "/auth/callback"
SCOPES = ["https://graph.microsoft.com/user.read"]
AUTHORITY = "https://login.microsoftonline.com/organizations"
VALID_EMAIL_DOMAINS = ""

LOGOUT_URL = AUTHORITY + "/oauth2/v2.0/logout"  # should this be URI?

# MS graph url
GRAPH_URL = "https://graph.microsoft.com/v1.0"  # whatever it was

# session constants.
TOKEN_CACHE = "token_cache"

# after ms login (django findable redirect)
INDEX_REDIRECT = "Index"
