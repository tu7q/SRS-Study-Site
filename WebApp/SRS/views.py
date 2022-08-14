from types import NoneType
from typing import List
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

from . import models
from .models import Assesment
from .models import QuestionTuple

CURRENT_QUESTION = "CURRENT_QUESTION"


def valid_standard(standard: str) -> bool:
    val = Assesment.standard.get(standard, None)
    return type(val) != NoneType


def get_assesment_model(standard: str) -> Type[Assesment]:
    return Assesment.assesments[Assesment.standards[standard]]


def get_question(request: HttpRequest, standard: str) -> QuestionTuple:
    question = request.session.get(CURRENT_QUESTION)
    if question is None:
        model = get_assesment_model(standard)
        assesment = model.objects.get_or_create(user=request.user)
        question = assesment.next_question()
        request.session[CURRENT_QUESTION] = question
    return question


class ListAssesmentsView(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest):
        return render(
            request,
            "SRS/assesments.html",
            context={"assesments": Assesment.assesments},
        )


class Question(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: str = None) -> HttpResponse:
        if not valid_standard(standard):
            raise Http404
        question = get_question(request, standard)
        return render(request, "SRS/question.html", context={"question": question})


class Answer(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: str = None):
        if not valid_standard(standard):
            raise Http404
        question = get_question(request, standard)
        if question:
            answer = question.val.model_answer()
            return JsonResponse({"model_answer": answer})
        raise HttpResponseGone


class Mark(View):
    @method_decorator(login_required)
    def get(self, request: HttpRequest, standard: str = None):
        if not valid_standard(standard):
            raise Http404
        score = request.GET.get("score", None)
        if not score:
            raise HttpResponseBadRequest
        question = get_question(request, standard)
        if not question:
            raise HttpResponseBadRequest
        question.val.update(score)

        attrname, question = request.session.get("current_question")
        if not question:
            raise HttpResponseBadRequest
        question.update(score)
        model = get_assesment_model(standard)
        assesment = model.objects.get(user=request.user)
        setattr(assesment, attrname, question.val)
        request.session.pop("current_question")
        model.save()
        return redirect("Question")

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
