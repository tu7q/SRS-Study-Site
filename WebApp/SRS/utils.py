# Responsible for application logic
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from django.contrib.sessions.backends.base import SessionBase
from typing import Dict, Literal, Optional, List, Type


@dataclass
class _Subject:
    name: str
    level: Literal[1, 2, 3]


class Subject(str, Enum):
    chemistry = _Subject(name="chemistry", level=3)
    calculus = _Subject(name="calculus", level=3)
    physics = _Subject(name="physics", level=3)


@dataclass
class _Assesment:
    name: str
    type: Literal["internal", "external"]


class AssesmentBase(str, Enum):
    _ignore_: str | list[str] = "all"
    all: Dict[
        Subject, AssesmentBase
    ] = {}  # will not be discarded by the Enum meta class. (Only useful for type checker)

    def __init_subclass__(cls, subject: Subject = None) -> None:
        return super().__init_subclass__()
        if subject is not None:
            cls.all[subject] = cls

    @classmethod
    def subject_assesments(cls, subject: Subject) -> List[AssesmentBase]:
        subject = cls.all[subject]
        assesments = []
        for assesment in subject:
            assesments.append(assesment)
        return assesment


# Note:
AssesmentBase.all = {}


class ChemistryAssesments(AssesmentBase, subject=Subject.chemistry):
    organic = _Assesment(name="organic", type="external")
    spectroscopy = _Assesment(name="organic", type="external")
    redux = _Assesment(name="organic", type="internal")


class PhysicsAssesments(AssesmentBase, subject=Subject.physics):
    waves = _Assesment(name="waves", type="external")
    mechanics = _Assesment(name="mechanics", type="external")


class CalculusAssesments(AssesmentBase, subject=Subject.calculus):
    differentiation = _Assesment(name="differentiation", type="external")
    integration = _Assesment(name="integration", type="external")
    complex_algebra = _Assesment(name="complex algebra", type="external")


class QuestionBase:
    """The base Subject class from which all questions derrive"""

    """Should questions be stored or should they be generated through RNG(?)"""

    all: Dict[AssesmentBase, List[Type[QuestionBase]]] = {}

    def __init_subclass__(cls, assesment: AssesmentBase = None) -> None:
        super().__init_subclass__()
        if assesment is not None:
            cls.all.setdefault(assesment, [])
            cls.all[assesment].append(cls)

    @classmethod
    def assesment_questions(cls, assesment: AssesmentBase) -> Type[QuestionBase]:
        """Gets all of the questions associated with an assesment"""
        return cls.all[assesment]

    def __init__(self, **kwargs) -> None:
        pass

    def _generate(self):
        """Generates a new question"""
        pass

    def get_model_answer(self) -> Dict:
        raise NotImplementedError("base class has no answers")

    @classmethod
    def from_json(cls, json) -> QuestionBase:
        """Returns the object from JSON into an object"""
        return cls(**json)

    def json(self):
        """turns the question into JSON for storage"""
        raise NotImplementedError("base question class can't be stored")


class OrganicChemistryQuestion(QuestionBase, assesment=ChemistryAssesments.organic):
    def _generate(self):
        pass

    def fill(self, data) -> None:
        pass

    def mark(self) -> Dict:
        pass


class DifferntiationCalculusQuestion(QuestionBase, assesment=CalculusAssesments.differentiation):
    def _generate(self):
        pass

    def fill(self, data) -> None:
        pass

    def mark(self) -> Dict:
        pass


""" Other Questions """


# def all_subjects() -> bool:
#     return list(map(lambda x: x.lower(), QuestionBase.questions.keys()))


# def get_or_create_question(subject: str, session: SessionBase) -> Optional[QuestionBase]:
#     """Assumes that subject is a valid subject."""
#     # try getting the question from the session
#     question = session.get(subject, None)
#     if question:
#         return question
#     # else create the session
#     question_type = QuestionBase.questions.get(subject)
#     # in this case it needs to access the queue mechanism and retreive the most recent element.
#     return question_type()


# logs in
# redirects to question
# gets next quesiton based on database -> question.html
# answers question -> result: json

# the question being answered by the user is stored into session
#
