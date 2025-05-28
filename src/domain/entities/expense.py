import re
from datetime import UTC, datetime
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
    date: datetime | None = Field(
        default_factory=lambda: datetime.now(UTC),
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
    def validate_date(cls, value: datetime | None) -> datetime:
        if not value:
            return datetime.now(UTC)

        if value > datetime.now(UTC):
            raise FutureDateException

        return value
