from __future__ import annotations
from enum import Enum, auto
from statistics import mean
from django.db import models
from MicrosoftAuth.models import User
import time
from typing import Any, Dict, Optional, Tuple, Type, List, Iterator
from . import questions as q
from .multifield import MultiField, MultiFieldBase
from datetime import datetime
from dataclasses import dataclass

# import inspect


def QuestionField(q_type: Type[q.QuestionInfo]) -> MultiField:
    def get(forbidden_until=None, last_score=None, seed=None) -> q.QuestionInfo:
        return q_type(forbidden_until=forbidden_until, last_score=last_score, seed=seed)

    def set(value: q.QuestionInfo) -> Dict[str, Any]:
        return {"forbidden_until": value.forbidden_until, "last_score": value.last_score, "seed": value.seed}

    return MultiField(
        get,
        set,
        forbidden_until=models.DateTimeField(blank=True),
        last_score=models.SmallIntegerField(blank=True),
        seed=models.IntegerField(blank=True),
    )


class Subject(Enum):
    """
    Subjects don't express any behaviour other than to act as a category.
    """

    chemistry = auto()
    physics = auto()


class Assesment(MultiFieldBase):
    """Note: Is empty for reasons"""

    SUBJECT: Subject = None
    NAME: str = None
    STANDARD: str = None
    LEVEL: int = None

    registry: Dict[str, Type[Assesment]] = {subject: list() for subject in Subject}

    def __init_subclass__(cls) -> None:
        if isinstance(cls.SUBJECT, Subject):
            cls.registry[cls.SUBJECT].append(cls)
        return super().__init_subclass__()

    @classmethod
    def assesments(cls, subject: Subject) -> List[Type[Assesment]]:
        return cls.registry[subject]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    average_score = models.FloatField()

    class Meta:
        abstract = True

    def question_fields(self) -> Iterator[Tuple[str, q.QuestionInfo]]:  # technically Generator not Iterator
        for field_name in self.multifields:
            field = getattr(self, field_name)
            if isinstance(field, q.QuestionInfo):
                yield field_name, field

    def next_question(self) -> Optional[q.QuestionInfo]:
        most_recent = datetime.now()
        best = None
        for _, field in self.question_fields():
            if field.forbidden_until < most_recent:
                # field.forbidden_until is more recent than most_recent field
                most_recent = field.forbidden_until
                best = field
        # if best is None then none were more recent than the current date so there is no question to return.
        return best

    def get_average_score(self) -> float:
        scores = []
        for _, field in self.question_fields():
            scores.append(field.last_score)
        return mean(scores)

    def save(self, *args, **kwargs):
        self.average_score = round(self.get_average_score(), 2)  # round the average_score to 2 decimal places

        super().save(*args, **kwargs)


class AS91391(Assesment):
    SUBJECT = Subject.chemistry
    NAME = "Demonstrate understanding of the properties of organic compounds"
    STANDARD = 91391
    LEVEL = 3

    some_question = QuestionField(q.SomeChemistryQuestion)
    other_question = QuestionField(q.SomeChemistryQuestion)


# print('dir: [', dir(AS91391), ']\n')
# print('__dict__: [', AS91391.__dict__, ']\n')
# some_question = q.SomeChemistryQuestion(
#     forbidden_until=datetime.now(),
#     last_score=2,
#     seed=time.time()
# )
# other_question = q.SomeChemistryQuestion(
#     forbidden_until=datetime.now(),
#     last_score=2,
#     seed=time.time()
# )
# assesment1 = AS91391(some_question=some_question, other_question=other_question)
# print('obj1', assesment1, 'type:', type(assesment1))
# assesment2 = AS91391(
#     some_question_forbidden_until=some_question.forbidden_until,
#     some_question_last_score=some_question.last_score,
#     some_question_seed=some_question.seed,
#     other_question_forbidden_until=other_question.forbidden_until,
#     other_question_last_score=other_question.last_score,
#     other_question_seed=other_question.seed
# )
# print('obj2', assesment2)
# assesment3 = AS91391(
#     some_question_forbidden_until=some_question.forbidden_until,
#     some_question_last_score=some_question.last_score,
#     some_question_seed=some_question.seed,
#     other_question_forbidden_until=other_question.forbidden_until,
#     other_question_last_score=other_question.last_score,
#     other_question_seed=other_question.seed
# )
# print('obj3', assesment3)
# assesment4 = AS91391(
#     some_question=some_question,
#     other_question_forbidden_until=other_question.forbidden_until,
#     other_question_last_score=other_question.last_score,
#     other_question_seed=other_question.seed
# )
# print('obj4', assesment4)
# assesment5 = AS91391(
#     other_question=other_question,
#     some_question_forbidden_until=some_question.forbidden_until,
#     some_question_last_score=some_question.last_score,
#     some_question_seed=some_question.seed,
# )
# print('obj5', assesment5)
# assesment6 = AS91391(
#     other_question=other_question,
#     some_question=some_question, # Note: it overides the values specified below (if they were different objects)
#     some_question_forbidden_until=some_question.forbidden_until,
#     some_question_last_score=some_question.last_score,
#     some_question_seed=some_question.seed,
# )
# print('obj6', assesment6)
# assesment7 = AS91391(
#     other_question=other_question # ignore some_question
# )
# print('obj7', assesment7)
# assesment8 = AS91391(
#     some_question=some_question # ignore other_question
# )
# print('obj8', assesment8)
