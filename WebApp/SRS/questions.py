from dataclasses import dataclass
from datetime import datetime

# import random


@dataclass
class QuestionInfo:
    forbidden_until: datetime
    last_score: int
    seed: int

    @property
    def title(self) -> str:
        raise NotImplementedError("QuestionInfo base doesn't support title property")

    @property
    def content(self) -> str:
        raise NotImplementedError("QuestionInfo base doesn't support content property")

    @property
    def model_answer(self) -> str:
        raise NotImplementedError("QuestionInfo base doesn't support model_answer property")


class SomeChemistryQuestion(QuestionInfo):
    @property
    def title(self) -> str:
        return "Some Chemistry Question"

    @property
    def content(self) -> str:
        return "Hello there!\n" "How are you?\n" "Thats good I suppose."

    @property
    def model_answer(self) -> str:
        return "As according to legend passed down throughout the ages\n" "The answer is ...\n" "2!!"
