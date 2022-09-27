from django.urls import path

from . import views

urlpatterns = [
    path(
        "",
        views.ListAssesmentsView.as_view(),
        name="Index"
        # name="AssesmentViews",
    ),  # view all assesments
    path("assesment/<int:standard>/", views.QuestionView.as_view(), name="QuestionView"),  # view/answer questions
    path("answer/<int:standard>/", views.AnswerView.as_view(), name="AnswerView"),  # view/answer questions
    path("mark/<int:standard>/<int:score>", views.MarkView.as_view(), name="MarkView"),  # view/answer questions
]
