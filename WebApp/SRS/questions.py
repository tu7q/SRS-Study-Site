from __future__ import annotations

import datetime
import time
from typing import Dict
from typing import Set
from typing import Type

from django.core.validators import MaxValueValidator
from django.core.validators import MinValueValidator
from django.db import models
from polymorphic.models import PolymorphicModel

from . import assesments

OFFSET = 1


def lockout_duration(score: int):
    # the higher the score the longer the duration (so the questions with lower score get returned more often)
    return datetime.timedelta(minutes=30 * score + OFFSET)


questions: Dict[assesments.Assesment, Set[Type[Question]]] = {}


def register_question(cls):
    questions.setdefault(cls.ASSESMENT, set())
    questions[cls.ASSESMENT].add(cls)
    return cls


class Question(PolymorphicModel):
    ASSESMENT: Type[assesments.Assesment] = None

    SCORE_LB = 0  # lower bound
    SCORE_UB = 5  # upper bound

    assesment = models.ForeignKey(
        assesments.Assesment, related_name="questions", on_delete=models.CASCADE, db_index=True
    )
    forbidden_until = models.DateTimeField(default=datetime.datetime.min)
    last_score = models.SmallIntegerField(
        default=0, validators=[MaxValueValidator(SCORE_UB), MinValueValidator(SCORE_LB)]
    )
    seed = models.IntegerField(default=time.time)

    def mark(self, score: int) -> None:
        self.seed = time.time()  # reseed the question

        # force score to be a valid int. I don't mind dealing with otherwise invalid scores this way.
        if score < self.SCORE_LB:
            score = self.SCORE_LB
        elif score > self.SCORE_UB:
            score = self.SCORE_UB

        self.last_score = score
        self.forbidden_until = datetime.datetime.now() + lockout_duration(score)

    @property
    def title(self) -> str:
        raise NotImplementedError("QuestionInfo base doesn't support title property")

    @property
    def content(self) -> str:
        raise NotImplementedError("QuestionInfo base doesn't support content property")

    @property
    def model_answer(self) -> str:
        raise NotImplementedError("QuestionInfo base doesn't support model_answer property")


@register_question
class SomeQuestion(Question):
    ASSESMENT = assesments.AS91391

    class Meta:
        proxy = True

    @property
    def title(self) -> str:
        return "Some Question"

    @property
    def content(self) -> str:
        return "Some Question Content"

    @property
    def model_answer(self) -> str:
        return "Some Question Answer"


@register_question
class OtherQuestion(Question):
    ASSESMENT = assesments.AS91392

    class Meta:
        proxy = True

    @property
    def title(self) -> str:
        return "Other Question"

    @property
    def content(self) -> str:
        return "Other Question Content"

    @property
    def model_answer(self) -> str:
        return "Other Question Answer"


@register_question
class AnotherQuestion(Question):
    ASSESMENT = assesments.AS91392

    class Meta:
        proxy = True

    @property
    def title(self) -> str:
        return "Another Question"

    @property
    def content(self) -> str:
        return "Another Question Content"

    @property
    def model_answer(self) -> str:
        return "Another Question Answer"
