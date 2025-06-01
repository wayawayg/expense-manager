import re
import datetime
from decimal import Decimal
from uuid import uuid4

from pydantic import Field, field_validator

from src.domain.entities.base import BaseEntity
from src.domain.exceptions.expense import (
    AmountAccuracyTooLongException,
    CategoryTextTooLongException,
    DescriptionTextTooLongException,
    FutureDateException,
    NotPositiveAmountException,
)


class Expense(BaseEntity):
    user_id: int
    amount: Decimal
    category: str
    description: str | None = None
    date: datetime.date | None = Field(
        default_factory=datetime.date.today
    )

    @field_validator("amount", mode="after")
    @classmethod
    def validate_amount(cls, value: Decimal) -> Decimal:
        if value <= 0:
            raise NotPositiveAmountException

        if not re.fullmatch(r"^[0-9]\d*(?:\.\d{1,2})?$", str(value)):
            raise AmountAccuracyTooLongException

        return value

    @field_validator("category", mode="after")
    @classmethod
    def validate_category(cls, value: str) -> str:
        if len(value) > 100:
            raise CategoryTextTooLongException

        return value

    @field_validator("description", mode="after")
    @classmethod
    def validate_description(cls, value: str | None) -> str | None:
        if not value:
            return None

        if len(value) > 350:
            raise DescriptionTextTooLongException

        return value

    @field_validator("date", mode="after")
    @classmethod
    def validate_date(cls, value: datetime.date | None) -> datetime.date:
        if not value:
            return datetime.date.today()

        # TODO check tz date info
        if value > datetime.date.today():
            raise FutureDateException

        return value
