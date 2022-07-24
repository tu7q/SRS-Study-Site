from django.shortcuts import redirect, render
from django.http import (
    HttpRequest,
    HttpResponse,
    Http404,
    HttpResponseBadRequest,
    JsonResponse,
)
from django.views import View
from MicrosoftAuthentication.decorators import RequireMSAuthentication
from . import utils
from typing import List
from . import models

# List of possible subjects
# @RequireMSAuthentication
def Index(request: HttpRequest) -> HttpResponse:
    pass


class Question(View):
    # dispatcher: QuestionDispatcher = QuestionDispatcher()
    valid_subjects: List[str] = utils.all_subjects()

    # @RequireMSAuthentication
    def get(self, request: HttpRequest, subject: str = "") -> HttpResponse:
        subject = subject.lower()

        if subject not in Question.valid_subjects:
            raise Http404

        if subject in request.session:
            print("subject in session")
            question = request.session[subject]
        else:
            print("subject not in session")
            # models.next(subject)
            question = "hi!"
        request.session[subject] = question

        return HttpResponse(f"Hello There!")
        # return render("template", context={"question": question})

    # @RequireMSAuthentication
    def post(self, request: HttpRequest, subject: str = None) -> HttpResponse:
        subject = subject.lower()
        if subject not in Question.valid_subjects:
            raise Http404

        # clear and retrieve the subject from the session
        question = request.session.pop(subject, None)
        if question is None:  # didn't make get request so subject and question pair don't exist.
            raise HttpResponseBadRequest
        question.fill(request.POST)  # fill the question with the users answers.
        marked_question = question.mark()  # get the marked question

        models.return_to_queue(question)  # Question is not needed and is placed in the queue

        return JsonResponse(marked_question)
