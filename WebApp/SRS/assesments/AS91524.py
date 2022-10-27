import math
from random import Random

from ..models import Assesment
from ..models import ASType
from ..models import QAA


class AS91524(Assesment):
    NAME = "Demonstrate understanding of mechanical systems"
    STANDARD = 91524
    ASTYPE = ASType.External
    LEVEL = 3

    class Meta:
        proxy = True


class Q_1(QAA):
    """
    Centre of Mass:
    M1X1 = M2X2
    And velocity of COM:
    (V1M1 + V2M2) / (M1 + M2)
    """

    ASSESMENT = AS91524

    HEAD_TEMPLATE: str = "SRS/AS91524/Q_1/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91524/Q_1/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91524/Q_1/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        r = Random(self.seed)
        context["distance"] = r.randint(2, 10)
        context["M1"] = r.randint(2, 7)
        context["M2"] = r.randint(2, 7)
        context["computed"] = round((context["distance"] * context["M2"]) / (context["M1"] + context["M2"]), 1)

        return context


class Q_2(QAA):
    """
    Banking on Curves -> Critical Velocity
    """

    ASSESMENT = AS91524

    HEAD_TEMPLATE: str = "SRS/AS91524/Q_2/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91524/Q_2/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91524/Q_2/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        r = Random(self.seed)
        mass = r.randint(1000, 1300)
        radius = r.randint(30, 50)
        bank = r.randint(8, 18)

        Fg = mass * 9.81
        Fr = Fg / math.cos(math.radians(bank))
        Fn = math.sqrt((Fr**2) - (Fg**2))
        v = math.sqrt((Fn * radius) / (mass))

        context["mass"] = mass
        context["r"] = radius
        context["bank"] = bank
        context["Fg"] = round(Fg, 1)
        context["Fr"] = round(Fr, 1)
        context["Fn"] = round(Fn, 1)
        context["v"] = round(v, 1)

        return context


class Q_3(QAA):
    """
    Newtons Law of Gravitation
    """

    ASSESMENT = AS91524

    HEAD_TEMPLATE: str = "SRS/AS91524/Q_3/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91524/Q_3/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91524/Q_3/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        G = float("6.67e-11")

        r = Random(self.seed)
        v = r.randint(200, 300)
        T = r.randint(2000, 3000)  # 2000 - 3000 hours
        T_s = T * 60 * 60

        d = v * T_s
        radius = d / (2 * math.pi)
        M = (radius * (v**2)) / G

        context["G"] = G
        context["v"] = v
        context["T"] = T_s
        context["d"] = d
        context["r"] = radius
        context["M"] = M

        return context


class Q_4(QAA):
    """
    Vertical Circular Motion
    """

    ASSESMENT = AS91524

    HEAD_TEMPLATE: str = "SRS/AS91524/Q_4/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91524/Q_4/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91524/Q_4/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        g = 9.81

        r = Random(self.seed)

        # Note: +0.1 -> non 0
        M = round(r.random() * 8, 1) + 0.1  # 0 -> 8.
        radius = round(r.random() * 3, 1) + 0.1  # 0 -> 3. 1dp

        v = math.sqrt(g * radius)

        context["g"] = g
        context["M"] = round(M, 1)
        context["r"] = round(radius, 1)
        context["v"] = round(v, 1)

        return context


class Q_5(QAA):
    """
    Vertical Circular Motion
    """

    ASSESMENT = AS91524

    HEAD_TEMPLATE: str = "SRS/AS91524/Q_5/head.html"
    MODEL_ANSWER_TEMPLATE: str = "SRS/AS91524/Q_5/answer.html"
    QUESTION_TEMPLATE: str = "SRS/AS91524/Q_5/question.html"

    class Meta:
        proxy = True

    def context(self):
        context = {}

        g = 9.81

        r = Random(self.seed)
        m = r.randint(30, 60)
        radius = r.randint(15, 25)

        v = math.sqrt(g * radius)
        Ke = (0.5 * m * (v**2)) + (2 * m * g * radius)

        context["g"] = g
        context["m"] = m
        context["r"] = radius
        context["v"] = round(v, 1)
        context["Ke"] = round(Ke, 1)

        return context
