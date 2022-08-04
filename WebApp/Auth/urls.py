from django.urls import path
from . import views

urlpatterns = [
    path("", views.Login, name="Login"),
    path("callback", views.Callback, name="Callback"),
    path("logout/", views.Logout, name="Logout"),
]
