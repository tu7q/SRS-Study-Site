from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.ListAssesmentsView.as_view(),
        name="AssesmentViews",
    ),  # view all assesments
    path("question/<str:standard>/", views.Question.as_view(), name="QuestionView"),  # view/answer questions
    path("answer/<str:standard>/", views.Answer.as_view(), name="AnswerView"),  # view/answer questions
    path("mark/<str:standard>/", views.Mark.as_view(), name="MarkView"),  # view/answer questions
]
