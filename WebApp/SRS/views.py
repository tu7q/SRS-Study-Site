import datetime
import logging
import re
from contextlib import suppress
from types import NoneType
from typing import Any
from typing import List
from typing import Optional
from typing import Type

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
from django.http import QueryDict
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
    a_instance.last_accessed = datetime.datetime.now()
    question = a_instance.questions.earliest("forbidden_until")
    a_instance.save()
    if question.forbidden_until > datetime.datetime.now():
        raise NoAvailableQuestion()
    return question


def HXRedirect(url_name, **kwargs):
    response = HttpResponse()
    # response = redirect(url_name, **kwargs)
    response["HX-Redirect"] = reverse(url_name, kwargs=kwargs)
    return response


class ListAssesmentsView(View):
    PER_PAGE = 3
    MAX_QUERY_SIZE = 30

    @method_decorator(login_required)
    def get(self, request: HttpRequest):
        # Get GET paremeters
        params = QueryDict("", mutable=True)
        with suppress(KeyError, ValueError):
            params["page"] = int(request.GET["page"])
        with suppress(KeyError):
            search = request.GET["search"]
            if re.fullmatch("^[a-zA-Z0-9_]*$", search):  # if query is alphanumeric
                params["search"] = search

        if "page" not in params:
            # No page number. So display base page.
            # get extra context variables.
            recent = Assesment.objects.filter(user=request.user).order_by("-last_accessed")[:3]  # no list
            return render(request, "SRS/assesments.html", context={"recent_assesments": recent, "params": params})

        # otherwise: display search results.

        if params["search"]:
            filtered = [
                a for a, _ in m.assesment_table.search._search_term(params["search"], limit=self.MAX_QUERY_SIZE)
            ]
        else:
            filtered = m.assesment_table

        paginator = Paginator(filtered, per_page=self.PER_PAGE)
        assesments = paginator.page(params["page"])

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
