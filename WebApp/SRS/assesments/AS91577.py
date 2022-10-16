import math
from random import Random

from ..models import Assesment
from ..models import ASType
from ..models import QAA


class AS91577(Assesment):
    NAME = "Apply the algebra of complex numbers in solving problems"
    STANDARD = 91577
    ASTYPE = ASType.External
    LEVEL = 3

    class Meta:
        proxy = True


class Q_1(QAA):
    """
    Simplify quotients with surds by rationalising the denominator
    """

    ASSESMENT = AS91577

    HEAD_TEMPLATE: str = "SRS/AS91577/Q_1/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91577/Q_1/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91577/Q_1/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        r = Random(self.seed)

        a = r.randint(2, 9)
        b = r.randint(2, 9)
        c = r.randint(2, 9)

        top = float(math.sqrt(b * c) * a)
        val = float(top / c)

        if val.is_integer():
            context["simple"] = True
            context["val"] = val
        if top.is_integer():
            # can simplify
            context["simple_top"] = True
            context["top"] = top

        context["a"] = a
        context["b"] = b
        context["c"] = c
        context["bc"] = b * c

        return context


class Q_2(QAA):
    """
    Remainder and Factor Theorem
    """

    ASSESMENT = AS91577

    HEAD_TEMPLATE: str = "SRS/AS91577/Q_2/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91577/Q_2/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91577/Q_2/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        r = Random(self.seed)

        a = r.randint(2, 9)
        b = r.randint(2, 9)
        c = r.randint(2, 9)
        d = r.randint(2, 9)  # just keep it positive for simplicity

        # as in
        # x^2 + bx + c
        # divided by
        # (x + d)

        # x = -d
        r = a * (d**2) + -1 * b * d + c

        context["a"] = a
        context["b"] = b
        context["c"] = c
        context["d"] = d
        context["r"] = r
        context["ad2"] = a * (d**2)
        context["bd"] = b * d

        return context


class Q_3(QAA):
    """
    Complex number Excellence problem
    """

    ASSESMENT = AS91577

    HEAD_TEMPLATE: str = "SRS/AS91577/Q_3/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91577/Q_3/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91577/Q_3/question.html"

    class Meta:
        proxy = True


class Q_4(QAA):
    """
    Conjugate root pairs
    """

    ASSESMENT = AS91577

    HEAD_TEMPLATE: str = "SRS/AS91577/Q_4/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91577/Q_4/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91577/Q_4/question.html"

    class Meta:
        proxy = True


class Q_5(QAA):
    """
    Polar Form + Argand Diagram + De Moivre's Theorem
    """

    ASSESMENT = AS91577

    HEAD_TEMPLATE: str = "SRS/AS91577/Q_5/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91577/Q_5/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91577/Q_5/question.html"

    class Meta:
        proxy = True
