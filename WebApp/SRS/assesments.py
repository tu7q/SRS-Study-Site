from __future__ import annotations

import numbers
from enum import auto
from enum import Enum
from typing import Dict
from typing import List

from django.db import models
from MicrosoftAuth.models import User
from polymorphic.models import PolymorphicModel

assesments: List[Assesment] = []
standards: Dict[int, int] = {}


def register_assesment(cls):
    assesments.append(cls)
    standards[cls.STANDARD] = len(assesments) - 1  # last idx of assesments list
    return cls


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

    def save(self, *args, **kwargs):
        if not isinstance(self.avg_score, numbers.Number):
            self.avg_score = 0  # just set to something pointless for now

        super().save(*args, **kwargs)


@register_assesment
class AS91391(Assesment):
    NAME = "Demonstrate understanding of the properties of organic compounds"
    STANDARD = 91391
    ASTYPE = ASType.External
    LEVEL = 3

    class Meta:
        proxy = True


@register_assesment
class AS91392(Assesment):
    NAME = "Demonstrate understanding of equilibrium principles in aqueous systems"
    STANDARD = 91392
    ASTYPE = ASType.External
    LEVEL = 3

    class Meta:
        proxy = True
