from django.http import JsonResponse
from django.template.loader import get_template
from django_components.component import registry

from ..models import Assesment
from ..models import ASType
from ..models import QAA


class Test2(Assesment):
    NAME = "Test 2"
    STANDARD = 3
    ASTYPE = ASType.External
    LEVEL = 3

    class Meta:
        proxy = True


class Q_1(QAA):
    ASSESMENT = Test2

    MODEL_ANSWER_TEMPLATE: str = "SRS/questions/SomeQuestion_ma.html"
    QUESTION_TEMPLATE: str = "SRS/questions/SomeQuestion_q.html"

    class Meta:
        proxy = True

    def question_context(self):
        return {}

    def answer_context(self):
        return {}
