from __future__ import annotations

import datetime
import logging
import numbers
import time
from enum import auto
from enum import Enum
from typing import Type

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.template.loader import render_to_string
from MicrosoftAuth.models import User
from polymorphic.models import PolymorphicModel


class ASType(Enum):
    Internal = auto()
    External = auto()


class Assesment(PolymorphicModel):
    NAME: str = None
    STANDARD: int = None
    ASTYPE: ASType = None
    LEVEL: int = None

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    avg_score = models.FloatField()

    ALL = []
    FROM_STANDARDS = {}

    def __init_subclass__(cls) -> None:
        # warnings
        cls_name = cls.__name__
        if not isinstance(cls.NAME, str):
            logging.warning(f"class {cls_name} has not set NAME")
        if not isinstance(cls.STANDARD, int):
            logging.warning(f"class {cls_name} STANDARD is not an int")
        if not isinstance(cls.ASTYPE, ASType):
            logging.warning(f"class {cls_name} ASTYPE is not an ASType instance")
        if not isinstance(cls.LEVEL, int):
            logging.warning(f"class {cls_name} LEVEL is not an int")

        # logic
        cls.ALL.append(cls)
        cls.FROM_STANDARDS[cls.STANDARD] = len(cls.ALL) - 1  # last idx of assesments list

        return super().__init_subclass__()

    def save(self, *args, **kwargs):
        if not isinstance(self.avg_score, numbers.Number):
            # When avg_score is None or null force it to 0
            self.avg_score = 0  # just set to something pointless for now

        super().save(*args, **kwargs)


def lockout_duration(score: int) -> datetime.timedelta:
    # the higher the score the longer the duration (so the questions with lower score get returned more often)
    return datetime.timedelta(seconds=score) + lockout_duration.OFFSET


lockout_duration.OFFSET = datetime.timedelta(seconds=1)


class QAA(PolymorphicModel):
    """
    QAA -> Question and Answer. Renamed to better reflect its functionality since it wraps
    both question and answer part of a (Question?).
    """

    ASSESMENT: Type[Assesment] = None

    SCORE_LB = 0  # lower bound
    SCORE_UB = 5  # upper bound

    assesment = models.ForeignKey(Assesment, related_name="questions", on_delete=models.CASCADE, db_index=True)
    forbidden_until = models.DateTimeField(default=datetime.datetime.min)
    last_score = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(SCORE_UB), MinValueValidator(SCORE_LB)]
    )
    seed = models.IntegerField(default=time.time)

    ALL = {}

    def __init_subclass__(cls) -> None:
        # check the question
        if cls.ASSESMENT == None:
            logging.warning(f"class {cls.__name__} has not defined ASSESMENT.")

        # rename the class to avoid naming collisions
        cls.__name__ = cls.ASSESMENT.__name__ + "_" + cls.__name__

        cls.ALL.setdefault(cls.ASSESMENT, set())
        cls.ALL[cls.ASSESMENT].add(cls)

        return super().__init_subclass__()

    def mark(self, score: int) -> None:
        self.seed = time.time()  # reseed the question

        # force score to be a valid int. I don't mind dealing with otherwise invalid scores this way.
        if score < self.SCORE_LB:
            score = self.SCORE_LB
        elif score > self.SCORE_UB:
            score = self.SCORE_UB

        self.last_score = score
        self.forbidden_until = datetime.datetime.now() + lockout_duration(score)

    MODEL_ANSWER_TEMPLATE: str = None
    QUESTION_TEMPLATE: str = None

    def question_context(self):
        raise NotImplementedError()

    def answer_context(self):
        raise NotImplementedError()

    def render(self, question_content: bool = False, model_answer: bool = False) -> str:
        if model_answer and question_content:
            raise Exception("Question Content and Model Answer both selected")

        if question_content:
            context = self.question_context()
        if model_answer:
            context = self.answer_context()

        template = self.QUESTION_TEMPLATE
        if model_answer:
            template = self.MODEL_ANSWER_TEMPLATE

        return render_to_string(template, context, None, None)


from . import assesments
