from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.Login, name="Login"),
    path("callback/", views.Callback, name="Callback"),
    path("logout/", views.Logout, name="Logout"),
]
