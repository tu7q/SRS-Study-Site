from django.shortcuts import redirect, render
from django.http import HttpRequest, HttpResponse, Http404
from MicrosoftAuthentication.decorators import RequireMSAuthentication

ANSWERED_QUESTIONS = "ANSWERED_QUESTIONS"
QUESTIONS_PER_DAY = 10

# List of possible subjects
@RequireMSAuthentication
def Index(request: HttpRequest) -> HttpResponse:
    pass


def Question(request: HttpRequest, subject: str) -> HttpResponse:
    # is subject a valid subject
    if not Subject.objects.exists():
        raise Http404("Subject does not exist")

    if request.method == "POST":
        return question_post(request, subject)
    return question_get(request, subject)


# request.method is not neccesarily get
@RequireMSAuthentication
def question_get(request: HttpRequest, subject: str) -> HttpResponse:
    # load current question from session.
    answered_questions = request.session.get(ANSWERED_QUESTIONS, 0)
    if answered_questions >= QUESTIONS_PER_DAY:
        return render("finnished_today.html")
    # load next question
    next_question = ...
    context = {"": next_question}
    # return the question for answering
    return HttpResponse()


@RequireMSAuthentication
def question_post(request: HttpRequest, subject: str) -> HttpResponse:
    pass
    # get answer to question
    # check answer
    if request.session[ANSWERED_QUESTIONS] == None:
        request.session[ANSWERED_QUESTIONS] = 1
    else:
        request.session[ANSWERED_QUESTIONS] += 1
    # increase answered_questions
    # return result
