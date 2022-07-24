from django.urls import path
from . import views

urlpatterns = [
    path("", views.Index, name="Index"),
    path("question/<str:subject>/", views.Question.as_view(), name="Question"),
]
