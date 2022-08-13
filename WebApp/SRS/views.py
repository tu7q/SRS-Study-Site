from django.shortcuts import redirect, render
from django.http import (
    HttpRequest,
    HttpResponse,
    Http404,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.views import View
from typing import List
from . import models
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Subject
from .models import Assesment

# view list subjects
# returs subjects
# clicks a subject
# view list assesments
# returns assesments for a subject
# clicks assesment
# view Question
# returns a question to answer
# answer question
# view Answer
# returns a worked answer (in JSON)
# view Mark
# marks answer and returns next question

all_subjects = [s.name for s in Subject]

subject_to_assesments = {s.name: Assesment.assesments(s) for s in Subject}


class ListSubjectsView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, "SRS/subjects.html", context={"subjects": all_subjects})


class ListAssesmentsView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, subject: str = None):
        return render(request, "SRS/assesments.html", context={"assesments": subject_to_assesments[subject]})


class Question(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, assesment: str = None) -> HttpResponse:
        return render(request, "SRS/question.html")


class Answer(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, subject: str = None):
        pass


class Mark(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, subject: str = None):
        pass

    #     # subject = subject.lower()

    #     # if subject not in Question.valid_subjects:
    #     #     raise Http404

    #     # if subject in request.session:
    #     #     print("subject in session")
    #     #     question = request.session[subject]
    #     # else:
    #     #     print("subject not in session")
    #     #     # models.next(subject)
    #     #     question = "hi!"
    #     # request.session[subject] = question

    #     # return HttpResponse(f"Hello There!")
    #     # return render("template", context={"question": question})

    # @method_decorator(login_required)
    # def post(self, request: HttpRequest, assesment: str = None) -> HttpResponse:
    #     return JsonResponse({'hello': 5})
    #     pass
    #     # subject = subject.lower()
    #     # if subject not in Question.valid_subjects:
    #     #     raise Http404

    #     # # clear and retrieve the subject from the session
    #     # question = request.session.pop(subject, None)
    #     # if (
    #     #     question is None
    #     # ):  # didn't make get request so subject and question pair don't exist.
    #     #     raise HttpResponseBadRequest
    #     # question.fill(request.POST)  # fill the question with the users answers.
    #     # marked_question = question.mark()  # get the marked question

    #     # models.return_to_queue(
    #     #     question
    #     # )  # Question is not needed and is placed in the queue

    #     # return JsonResponse(marked_question)
