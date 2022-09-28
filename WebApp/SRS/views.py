import datetime
from msilib.schema import ListView
from tkinter import CURRENT
from types import NoneType
from typing import Any
from typing import List
from typing import Optional
from typing import Type
from xmlrpc.client import _datetime_type

import SRS.models as m
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import Http404
from django.http import HttpRequest
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseGone
from django.http import JsonResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import Assesment
from .models import QAA

# from django.utils import timezone


def valid_standard(standard: int) -> bool:
    a = Assesment.FROM_STANDARDS.get(standard, None)
    return type(a) != NoneType


def get_assesment(standard: int):  # -> Optional[Type[assesments.Assesment]]:
    return Assesment.ALL[Assesment.FROM_STANDARDS[standard]]
    # return assesments.assesments[assesments.standards[standard]]


class NoAvailableQuestion(Exception):
    pass


def get_question(request, standard):  # this is the first time the user is accessing the assesment
    # note replace this with signals (because they're cleaner)
    a_model = get_assesment(standard)
    a_instance, _ = a_model.objects.get_or_create(user=request.user)
    question = a_instance.questions.earliest("forbidden_until")
    if question.forbidden_until > datetime.datetime.now():
        raise NoAvailableQuestion()
    return question


def HXRedirect(url_name, **kwargs):
    response = redirect(url_name, **kwargs)
    response["HX-Redirect"] = reverse(url_name, kwargs=kwargs)
    return response


class ListAssesmentsView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest):
        # if 'results' in request.GET and request.GET['results']:

        level = request.GET.get("level")
        if level:
            level = int(level)

        params = request.GET.copy()
        params.pop("page", None)  # just remove it.

        if not "page" in request.GET:
            return render(request, "SRS/assesments.html", context={"params": params})
        page_n = int(request.GET["page"])

        MAX = 30

        term = request.GET.get("search", None)
        filtered = []

        if term:
            for assesment, score in m.assesment_table.search._search_term(term, limit=MAX):
                filtered.append(assesment)
        else:
            for i, assesment in enumerate(m.assesment_table):
                if i > 30:
                    break
                filtered.append(assesment)

        paginator = Paginator(filtered, per_page=3)
        assesments = paginator.page(page_n)

        return render(
            request,
            "SRS/assesments_page.html",
            context={"assesments": assesments, "params": params},
        )


class QuestionView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: int = None) -> HttpResponse:
        if not valid_standard(standard):
            raise Http404()
        try:
            question = get_question(request, standard)
        except NoAvailableQuestion:
            a_model = get_assesment(standard)
            a_instance, created = a_model.objects.get_or_create(user=request.user)
            question = a_instance.questions.earliest("forbidden_until")
            return render(request, "SRS/no_question.html", context={"next_question": question})
        return render(
            request,
            "SRS/question.html",
            context={"question": question, "standard": standard},  # ,
        )

    # def put(self, request: HttpRequest, standard: int = None) -> HttpResponse:
    #     # does this even get called? Can't remember.
    #     if not valid_standard(standard):
    #         raise Http404()
    #     try:
    #         q = get_question(request, standard)
    #     except NoAvailableQuestion:
    #         a_model = get_assesment(standard)
    #         a_instance, created = a_model.objects.get_or_create(user=request.user)
    #         question = a_instance.questions.earliest("forbidden_until")
    #         return render(request, "SRS/no_question.html", context={'next_question': question})
    #     return HttpResponse("<p>This is a response</p>")


class AnswerView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: int = None):
        if not valid_standard(standard):
            raise Http404()
        try:
            question = get_question(request, standard)
        except NoAvailableQuestion:
            return HttpResponseGone()
        return HttpResponse(question.render(as_answer=True))


class MarkView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: int = None, score: int = None):
        if not valid_standard(standard):
            raise Http404()
        try:
            question = get_question(request, standard)
        except NoAvailableQuestion:
            return HttpResponseBadRequest()
        question.mark(score)
        question.save()
        return HXRedirect("QuestionView", standard=standard)

        # return redirect("QuestionView", standard=standard)
        # return HttpResponse(status=204, headers={'HX-Redirect': reverse('QuestionView', kwargs={'standard': standard})})
