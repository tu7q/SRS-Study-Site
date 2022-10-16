from __future__ import annotations

import datetime
import logging
import numbers
import time
from enum import auto
from enum import Enum
from re import T
from typing import Type

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from django.template.exceptions import TemplateDoesNotExist
from django.template.exceptions import TemplateSyntaxError
from django.template.loader import render_to_string
from MicrosoftAuth.models import User
from polymorphic.models import PolymorphicModel


class ASType(Enum):
    Internal = auto()
    External = auto()


import littletable as lt

assesment_table = lt.Table("assesments")
assesment_table.create_index("STANDARD", unique=True)


class Assesment(PolymorphicModel):
    NAME: str = None
    STANDARD: int = None
    ASTYPE: ASType = None
    LEVEL: int = None

    user = models.ForeignKey(User, on_delete=models.CASCADE, db_index=True)
    last_accessed = models.DateTimeField(default=datetime.datetime.now, null=True)
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

        cls._search_term = " ".join([str(cls.STANDARD), "AS" + str(cls.STANDARD), cls.NAME])

        # Add the associated assesment into the table.
        assesment_table.insert(cls)
        assesment_table.create_search_index("_search_term")  # build/rebuild the search index

        # logic
        cls.ALL.append(cls)
        cls.FROM_STANDARDS[cls.STANDARD] = len(cls.ALL) - 1  # last idx of assesments list

        return super().__init_subclass__()

    # def add_score(self, next_score):
    #     self.avg_score = ((self.avg_score * self.attempts) + next_score) / (self.attempts + 1)
    #     self.attempts += 1
    #     self.save()

    def save(self, *args, **kwargs):
        if not isinstance(self.avg_score, numbers.Number):
            # When avg_score is None or null force it to 0
            self.avg_score = 0  # just set to something pointless for now

        super().save(*args, **kwargs)


def lockout_duration(score: int) -> datetime.timedelta:
    # the higher the score the longer the duration (so the questions with lower score get returned more often)
    return datetime.timedelta(minutes=score * 10) + lockout_duration.OFFSET


lockout_duration.OFFSET = datetime.timedelta(minutes=5)


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
        # rename the class to avoid naming collisions
        cls.__name__ = "AS" + str(cls.ASSESMENT.STANDARD) + "_" + cls.__name__

        # check the question
        if cls.ASSESMENT == None:
            logging.warning(f"class {cls.__name__} has not defined ASSESMENT.")

        if cls.HEAD_TEMPLATE == None:
            logging.warning(f"class {cls.__name__} has not defined HEAD_TEMPALTE.")

        if cls.QUESTION_TEMPLATE == None:
            logging.warning(f"class {cls.__name__} has not defined QUESTION_TEMPLATE.")

        if cls.MODEL_ANSWER_TEMPLATE == None:
            logging.warning(f"class {cls.__name__} has not defined MODEL_ANSWER_TEMPLATE.")

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

        # self.assesment.add_score(score)

    HEAD_TEMPLATE: str = None
    MODEL_ANSWER_TEMPLATE: str = None
    QUESTION_TEMPLATE: str = None

    def context(self):
        return {}

    def render(self, context={}, as_head=False, as_question: bool = False, as_answer: bool = False) -> str:
        request = context.get("request", None)  # important

        as_head = context.get("as_head", False) or as_head
        as_question = context.get("as_question", False) or as_question
        as_answer = context.get("as_answer", False) or as_answer

        if [as_head, as_question, as_answer].count(True) > 1:
            raise Exception("Only head, question_content or model_answer can't be used simultaneously")
        elif [as_head, as_question, as_answer].count(True) == 0:
            raise Exception("as_head or as_question or as_answer not provided to assesment render.")

        template = None
        if as_head:
            template = self.HEAD_TEMPLATE
        if as_question:
            template = self.QUESTION_TEMPLATE
        if as_answer:
            template = self.MODEL_ANSWER_TEMPLATE
        if template is None:
            return ""

        context = self.context()
        context["request"] = request

        try:
            return render_to_string(template, context, None, None)
        except TemplateDoesNotExist as e:
            logging.warning(f"Template: {template} does not exist and could not rendered")
            raise RuntimeError(f"Template: {template} does not exist and could not rendered") from e
        except TemplateSyntaxError as e:
            logging.warning(f"Assesment Template: {template} failed to render with context: {context}")
            raise RuntimeError(f"Assesment Template: {template} failed to render with context: {context}") from e


from . import assesments
