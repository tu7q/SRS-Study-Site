import datetime
from tkinter import CURRENT
from types import NoneType
from typing import Any
from typing import List
from typing import Optional
from typing import Type

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseGone
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View

from . import assesments
from . import questions

# from django.utils import timezone


def valid_standard(standard: int) -> bool:
    a = assesments.standards.get(standard, None)
    return type(a) != NoneType


def get_assesment(standard: int) -> Optional[Type[assesments.Assesment]]:
    return assesments.assesments[assesments.standards[standard]]


class NoAvailableQuestion(Exception):
    pass


def question_from_db(request, standard):  # this is the first time the user is accessing the assesment
    a_model = get_assesment(standard)
    a_instance, created = a_model.objects.get_or_create(user=request.user)

    if created:
        qs = (q_model.objects.create(assesment=a_instance) for q_model in questions.questions[a_model])
        question = min(qs, key=lambda q: q.forbidden_until)
    else:
        question = a_instance.questions.earliest("forbidden_until")
        # qs = a_instance.questions.all()
        # question = min(qs, key=lambda q: q.forbidden_until)
    if question.forbidden_until > datetime.datetime.now():
        raise NoAvailableQuestion()
    return question


def get_question(request: HttpRequest, standard: int, from_session=False) -> Optional[Any]:
    session_key = str(standard)
    if from_session:
        try:
            pk = request.session[session_key]
            return questions.Question.objects.get(pk=pk)
        except KeyError:
            raise NoAvailableQuestion()
    # models.Assesment
    if session_key in request.session:
        pk = request.session.get(session_key)
        question = questions.Question.objects.get(pk=pk)
    else:
        question = question_from_db(request, standard)
        request.session[session_key] = question.pk
    return question


class ListAssesmentsView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest):
        print(assesments.assesments)
        return render(
            request,
            "SRS/assesments.html",
            context={"assesments": assesments.assesments},
        )


class Question(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: int = None) -> HttpResponse:
        if not valid_standard(standard):
            raise Http404()
        try:
            question = get_question(request, standard)
        except NoAvailableQuestion:
            return render(request, "SRS/no_question.html")
        return render(request, "SRS/question.html", context={"question": question, "standard": standard})


class Answer(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: int = None):
        if not valid_standard(standard):
            raise Http404()
        try:
            question = get_question(request, standard, from_session=True)
        except NoAvailableQuestion:
            return HttpResponseGone()

        return JsonResponse({"model_answer": question.model_answer})


class Mark(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: int = None, score: int = None):
        if not valid_standard(standard):
            raise Http404()
        try:
            question = get_question(request, standard, from_session=True)
        except NoAvailableQuestion:
            return HttpResponseBadRequest()
        del request.session[str(standard)]  # this is the end of session so remove from here.
        question.mark(score)
        question.save()
        return redirect("QuestionView", standard=standard)
