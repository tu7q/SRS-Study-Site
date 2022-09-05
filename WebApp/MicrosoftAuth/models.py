from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.utils.crypto import get_random_string, salted_hmac
from django.utils import timezone


class UserManager(models.Manager):
    def _create_user(self, email, name, **extra_fields):
        pass

    def create_user(self, email, name):
        pass

    def create_superuser(self, email, name):
        pass

    @classmethod
    def normalize_email(cls, email):
        """
        Normalize the email address by lowercasing the domain part of it.
        """
        email = email or ""
        try:
            email_name, domain_part = email.strip().rsplit("@", 1)
        except ValueError:
            pass
        else:
            email = email_name + "@" + domain_part.lower()
        return email


class User(PermissionsMixin):
    REQUIRED_FIELDS = ()
    USERNAME_FIELD = "email"

    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(max_length=255, unique=True)

    last_login = models.DateTimeField("last login", blank=True, null=True)
    date_joined = models.DateTimeField("date joined", default=timezone.now)

    is_active = models.BooleanField(
        "active",
        default=True,
        help_text="Designates whether this user should be treated as active. "
        "Unselect this instead of deleting accounts.",
    )

    models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )

    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def natural_key(self):
        pass

    def get_email(self):
        return self.email

    def get_name(self):
        return self.name

    @property
    def is_anonymous(self):
        """
        Always return False. This is a way of comparing User objects to
        anonymous users.
        """
        return False

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

    def get_session_auth_hash(self):
        """
        Return an HMAC of the password field.
        """
        key_salt = "MicrosoftAuth.models.User.get_session_auth_hash"
        return salted_hmac(
            key_salt,
            self.email,
            algorithm="sha256",
        ).hexdigest()
