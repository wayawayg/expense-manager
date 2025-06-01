import datetime
from decimal import Decimal
from uuid import uuid4

import pytest

from src.domain.entities.expense import Expense
from src.domain.exceptions.expense import (
    AmountAccuracyTooLongException,
    CategoryTextTooLongException,
    DescriptionTextTooLongException,
    FutureDateException,
    NotPositiveAmountException,
)


def test_create_expense_with_too_long_amount_accuracy() -> None:
    current_date = datetime.date.today()

    with pytest.raises(AmountAccuracyTooLongException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("12.3456789"),
            category="Some category",
            description="Some description",
            date=current_date,
        )

    ex.value.message == "The accuracy of the amount should not exceed two decimal places."


def test_create_expense_with_negative_amount() -> None:
    current_date = datetime.date.today()

    with pytest.raises(NotPositiveAmountException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("-12.34"),
            category="Some category",
            description="Some description",
            date=current_date,
        )

    ex.value.message == "The amount spent cannot be negative or equal to zero."


def test_create_expense_with_zero_amount() -> None:
    current_date = datetime.date.today()

    with pytest.raises(NotPositiveAmountException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("0"),
            category="Some category",
            description="Some description",
            date=current_date,
        )

    ex.value.message == "The amount spent cannot be negative or equal to zero."


def test_create_expense_with_too_long_accuracy_negative_amount() -> None:
    current_date = datetime.date.today()

    with pytest.raises(NotPositiveAmountException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("-12.3456789"),
            category="Some category",
            description="Some description",
            date=current_date,
        )

    ex.value.message == "The amount spent cannot be negative or equal to zero."


def test_create_expense_with_too_long_category() -> None:
    current_date = datetime.date.today()

    with pytest.raises(CategoryTextTooLongException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("12.34"),
            category="a" * 101,
            description="Some description",
            date=current_date,
        )

    ex.value.message == "The category name is too long. A maximum of 100 characters is possible"


def test_create_expense_with_too_long_description() -> None:
    current_date = datetime.date.today()

    with pytest.raises(DescriptionTextTooLongException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("12.34"),
            category="Some category",
            description="a" * 351,
            date=current_date,
        )

    ex.value.message == "The description text is too long. A maximum of 350 characters is possible"


def test_create_expense_with_none_description() -> None:
    current_date = datetime.date.today()

    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        date=current_date,
        description=None,
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("12.34")
    assert expense.category == "Some category"
    assert not expense.description
    assert expense.date == current_date
    assert expense.created_at


def test_create_expense_without_description() -> None:
    current_date = datetime.date.today()

    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        date=current_date,
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("12.34")
    assert expense.category == "Some category"
    assert not expense.description
    assert expense.date == current_date
    assert expense.created_at


def test_create_expense_with_future_date() -> None:
    current_date = datetime.date.today()

    with pytest.raises(FutureDateException) as ex:
        expense = Expense(
            user_id=111,
            amount=Decimal("12.34"),
            category="Some category",
            description="Some description",
            date=current_date + datetime.timedelta(days=12),
        )

    ex.value.message == "This is a date that has not yet occurred"


def test_create_expense_with_none_date() -> None:
    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        description="Some description",
        date=None,
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("12.34")
    assert expense.category == "Some category"
    assert expense.description == "Some description"
    assert expense.date
    assert expense.created_at


def test_create_expense_without_date() -> None:
    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        description="Some description",
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("12.34")
    assert expense.category == "Some category"
    assert expense.description == "Some description"
    assert expense.date
    assert expense.created_at


def test_create_expense_success() -> None:
    current_date = datetime.date.today()

    # Average values
    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        description="Some description",
        date=current_date,
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("12.34")
    assert expense.category == "Some category"
    assert expense.description == "Some description"
    assert expense.date == current_date
    assert expense.created_at

    # Boundary values for the category and description
    expense = Expense(
        user_id=111,
        amount=Decimal("12"),
        category="a" * 100,
        description="b" * 350,
        date=current_date,
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("12")
    assert expense.category == "a" * 100
    assert expense.description == "b" * 350
    assert expense.date == current_date
    assert expense.created_at

    # Without a description
    expense = Expense(
        user_id=111,
        amount=Decimal("99999.5"),
        category="a",
        date=current_date,
    )

    assert expense.id
    assert expense.user_id == 111
    assert expense.amount == Decimal("99999.5")
    assert expense.category == "a"
    assert not expense.description
    assert expense.date == current_date
    assert expense.created_at
