from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path("", views.Login, name="MSLogin"),
    path("callback/", views.Callback, name="MSCallback"),
    path("logout/", views.Logout, name="MSLogout"),
]
