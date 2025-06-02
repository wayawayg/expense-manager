import datetime
from decimal import Decimal

from src.domain.entities.expense import Expense
from src.logic.repositories.expense import InMemoryExpenseRepository


def test_add_expense() -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)
    current_date = datetime.date.today()
    expense = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        description="Some description",
        date=current_date,
    )

    repo.add(expense)

    assert repo._storage == [expense]


def test_get_all_expenses() -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)
    current_date = datetime.date.today()

    expense1 = Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category1",
        description="Some description1",
        date=current_date,
    )
    expense2 = Expense(
        user_id=1,
        amount=Decimal("54.32"),
        category="Some category",
    )
    expense3 = Expense(
        user_id=111,
        amount=Decimal("76.88"),
        category="Some category3",
        description="Some description3",
        date=current_date,
    )
    expense4 = Expense(
        user_id=111,
        amount=Decimal("24.22"),
        category="Some category",
    )
    expense5 = Expense(
        user_id=7,
        amount=Decimal("796.88"),
        category="Some category3",
        description="Some description3",
        date=current_date,
    )

    repo.add(expense1)
    repo.add(expense2)
    repo.add(expense3)
    repo.add(expense4)
    repo.add(expense5)

    expenses = repo.get_all(
        user_id=111,
        limit=2,
        offset=1,
    )

    assert len(expenses) == 2
    assert expenses[0].user_id == 111
    assert expenses[0].amount == Decimal("76.88")
    assert expenses[0].category == "Some category3"
    assert expenses[0].description == "Some description3"
    assert expenses[0].date == current_date
    assert expenses[0].id
    assert expenses[0].created_at
    assert expenses[1].user_id == 111
    assert expenses[1].amount == Decimal("24.22")
    assert expenses[1].category == "Some category"
    assert not expenses[1].description
    assert expenses[1].date
    assert expenses[1].id
    assert expenses[1].created_at
