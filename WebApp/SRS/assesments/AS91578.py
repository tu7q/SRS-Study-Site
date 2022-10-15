from ..models import Assesment
from ..models import ASType
from ..models import QAA


class AS91578(Assesment):
    NAME = "Demonstrate understanding of mechanical systems"
    STANDARD = 90521
    ASTYPE = ASType.External
    LEVEL = 3

    class Meta:
        proxy = True


class Q_1(QAA):
    ASSESMENT = AS91578

    HEAD_TEMPLATE: str = "SRS/questions/SomeQuestion_head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/questions/SomeQuestion_ma.html"
    QUESTION_TEMPLATE: str = "SRS/questions/SomeQuestion_q.html"

    class Meta:
        proxy = True

    def question_context(self):
        return {}

    def answer_context(self):
        return {}
