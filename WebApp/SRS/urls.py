from django.urls import path
from . import views

urlpatterns = [
    path("", views.ListSubjectsView.as_view(), name="Index"),  # view subjects
    path("subject/<str:subject>", views.ListAssesmentsView.as_view(), name="Subject"),  # view questions in subjects
    path("question/<str:assesment>/", views.Question.as_view(), name="Question"),  # view/answer questions
]
