from django.apps import AppConfig
from django.conf import settings
from msal import PublicClientApplication

class MicrosoftauthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'MicrosoftAuthentication'

    def ready(self) -> None:
        app = PublicClientApplication(
            settings.MICROSOFT_APP['app_id']
        )
        
        return super().ready()