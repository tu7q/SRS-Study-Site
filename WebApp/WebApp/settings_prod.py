import os

from get_docker_secret import get_docker_secret

DEBUG = False

SECRET_KEY = get_docker_secret("secret_key")
if SECRET_KEY is None:
    raise RuntimeError("could not obtain the secret_key")

ALLOWED_HOSTS = ["ncea-srs.duckdns.org", "0.0.0.0", "localhost", "127.0.0.1", "raspberrypi"]

# GET Certificates for cookies to work again,
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
# SECURE_SSL_REDIRECT = True # Set reverse proxy to force HTTP requests

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_HOST"],
        "PORT": os.environ["DB_PORT"],
    }
}
