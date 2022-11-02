from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.Login.as_view(), name="Login"),
    path("callback/", views.Callback.as_view(), name="Callback"),
    path("logout/", views.Logout.as_view(), name="Logout"),
]
