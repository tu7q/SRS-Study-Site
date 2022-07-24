# Responsible for application logic
from __future__ import annotations
from django.contrib.sessions.backends.base import SessionBase
from typing import Dict, Optional


class QuestionBase:
    """The base Subject class from which all questions derrive"""

    all_questions: Dict[str, QuestionBase] = {}

    def __init__(self) -> None:
        self.filled_data = {}
        self.mark = {}

    def _generate(self):
        pass

    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)
        # QuestionBase.all_questions[cls.__name__] = cls
        cls.all_questions[cls.__name__] = cls

    def fill(self, data) -> None:  # POST data
        raise NotImplementedError("Base class can't fill answers")

    def mark(self) -> Dict:  # idk
        # when being marked a
        # self.__class__.__name__
        raise NotImplementedError("base class can't be checked")


class Chemistry(QuestionBase):
    def _generate(self):
        pass

    def fill(self, data) -> None:
        pass

    def mark(self) -> Dict:
        pass


""" Other Questions """


def all_subjects() -> bool:
    return list(map(lambda x: x.lower(), QuestionBase.all_questions.keys()))


def get_or_create_question(subject: str, session: SessionBase) -> Optional[QuestionBase]:
    """Assumes that subject is a valid subject."""
    # try getting the question from the session
    question = session.get(subject, None)
    if question:
        return question
    # else create the session
    question_type = QuestionBase.all_questions.get(subject)
    # in this case it needs to access the queue mechanism and retreive the most recent element.
    return question_type()


# logs in
# redirects to question
# gets next quesiton based on database -> question.html
# answers question -> result: json

# the question being answered by the user is stored into session
#
