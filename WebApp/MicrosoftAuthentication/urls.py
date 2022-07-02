from django.conf import settings
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
]
