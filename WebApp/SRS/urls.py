from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.ListAssesmentsView.as_view(),
        name="Index"
        # name="AssesmentViews",
    ),  # view all assesments
    path("question/<int:standard>/", views.Question.as_view(), name="QuestionView"),  # view/answer questions
    path("answer/<int:standard>/", views.Answer.as_view(), name="AnswerView"),  # view/answer questions
    path("mark/<int:standard>/<int:score>", views.Mark.as_view(), name="MarkView"),  # view/answer questions
]
