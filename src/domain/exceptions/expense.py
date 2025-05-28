from dataclasses import dataclass
from decimal import Decimal

from src.domain.exceptions.base import BaseException


@dataclass(eq=False, frozen=True, slots=True)
class AmountAccuracyTooLongException(BaseException):
    @property
    def message(self) -> str:
        return "The accuracy of the amount should not exceed two decimal places."


@dataclass(eq=False, frozen=True, slots=True)
class NotPositiveAmountException(BaseException):
    @property
    def message(self) -> str:
        return "The amount spent cannot be negative or equal to zero."


@dataclass(eq=True, frozen=True, slots=True)
class CategoryTextTooLongException(BaseException):
    @property
    def message(self) -> str:
        return "The category name is too long. A maximum of 100 characters is possible"


@dataclass(eq=True, frozen=True, slots=True)
class DescriptionTextTooLongException(BaseException):
    @property
    def message(self) -> str:
        return (
            "The description text is too long. A maximum of 350 characters is possible"
        )


@dataclass(eq=True, frozen=True, slots=True)
class FutureDateException(BaseException):
    @property
    def message(self) -> str:
        return "This is a date that has not yet occurred"
