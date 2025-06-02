import datetime
from decimal import Decimal

import pytest

from src.domain.entities.expense import Expense
from src.infra.mongo.config import expense_collection
from src.infra.mongo.repositories.expense import MongoExpenseRepository


@pytest.mark.asyncio
async def test_add_expense() -> None:
    repo = MongoExpenseRepository(expense_collection)
    current_date = datetime.date.today()
    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category1",
        description="Some description1",
        date=current_date,
    )

    id = await repo.add(expense)

    assert id


@pytest.mark.asyncio
async def test_get_all_expenses() -> None:
    repo = MongoExpenseRepository(expense_collection)
    current_date = datetime.date.today()
    expense1 = Expense(
        user_id=111,
        amount=Decimal("133.34"),
        category="Some category12",
        description="Some description12",
        date=current_date,
    )
    expense2 = Expense(
        user_id=123,
        amount=Decimal("76.88"),
        category="Some category3",
        description="Some description3",
        date=current_date,
    )
    expense3 = Expense(
        user_id=111,
        amount=Decimal("24.22"),
        category="Some category",
    )
    expense4 = Expense(
        user_id=7,
        amount=Decimal("796.88"),
        category="Some category3",
        description="Some description3",
        date=current_date,
    )

    await repo.add(expense1)
    await repo.add(expense2)
    await repo.add(expense3)
    await repo.add(expense4)
    expenses = await repo.get_all(111, 100, 0)

    assert len(expenses) == 2
    print(expenses)
    assert expenses[0].id
    assert expenses[0].user_id == 111
    assert expenses[0].amount == Decimal("133.34")
    assert expenses[0].category == "Some category12"
    assert expenses[0].date == current_date
    assert expenses[0].description == "Some description12"
    assert expenses[0].created_at
    assert expenses[1].id
    assert expenses[1].user_id == 111
    assert expenses[1].amount == Decimal("24.22")
    assert expenses[1].category == "Some category"
    assert expenses[1].date
    assert not expenses[1].description
    assert expenses[1].created_at
