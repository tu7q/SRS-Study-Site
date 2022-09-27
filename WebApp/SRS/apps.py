from django.apps import AppConfig


class SrsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "SRS"

    def ready(self):
        import SRS.signals
