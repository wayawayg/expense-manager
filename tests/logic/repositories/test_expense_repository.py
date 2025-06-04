import datetime
from decimal import Decimal

import pytest

from src.domain.entities.expense import Expense
from src.logic.repositories.expense import InMemoryExpenseRepository


@pytest.fixture
def current_date() -> datetime.date:
    return datetime.date.today()


@pytest.fixture
def expense1(current_date) -> Expense:
    return Expense(
        user_id=111,
        amount=Decimal("12.34"),
        category="Some category",
        description="Some description",
        date=current_date,
    )


@pytest.fixture
def expense2() -> Expense:
    return Expense(
        user_id=1,
        amount=Decimal("54.32"),
        category="Some category",
    )


@pytest.fixture
def expense3(current_date) -> Expense:
    return Expense(
        user_id=111,
        amount=Decimal("76.88"),
        category="Some category3",
        description="Some description3",
        date=current_date,
    )


@pytest.fixture
def expense4() -> Expense:
    return Expense(
        user_id=111,
        amount=Decimal("24.22"),
        category="Some category",
    )


@pytest.fixture
def expense5(current_date) -> Expense:
    return Expense(
        user_id=7,
        amount=Decimal("796.88"),
        category="Some category3",
        description="Some description3",
        date=current_date,
    )


@pytest.fixture
def expense1_user1() -> Expense:
    return Expense(
        user_id=1,
        amount=Decimal("12.34"),
        category="Cat1",
        date=datetime.date(
            year=2025,
            month=6,
            day=1,
        ),
    )


@pytest.fixture
def expense2_user1() -> Expense:
    return Expense(
        user_id=1,
        amount=Decimal("34.56"),
        category="Cat2",
        date=datetime.date(
            year=2025,
            month=6,
            day=2,
        ),
    )


@pytest.fixture
def expense3_user1() -> Expense:
    return Expense(
        user_id=1,
        amount=Decimal("56.78"),
        category="Cat2",
        date=datetime.date(
            year=2025,
            month=6,
            day=3,
        ),
    )


@pytest.fixture
def expense4_user1() -> Expense:
    return Expense(
        user_id=1,
        amount=Decimal("78.90"),
        category="Cat1",
        date=datetime.date(
            year=2025,
            month=5,
            day=31,
        ),
    )


@pytest.fixture
def expense5_user1() -> Expense:
    return Expense(
        user_id=1,
        amount=Decimal("98.76"),
        category="Cat3",
        date=datetime.date(
            year=2025,
            month=5,
            day=20,
        ),
    )


@pytest.mark.asyncio
async def test_add_expense(expense1) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)

    await repo.add(expense1)

    assert repo._storage == [expense1]


@pytest.mark.asyncio
async def test_get_all_expenses(
    expense1,
    expense2,
    expense3,
    expense4,
    expense5,
) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)

    await repo.add(expense1)
    await repo.add(expense2)
    await repo.add(expense3)
    await repo.add(expense4)
    await repo.add(expense5)

    expenses = await repo.get_all(
        user_id=111,
        limit=2,
        offset=1,
    )

    assert len(expenses) == 2
    assert expenses[0].user_id == 111
    assert expenses[0].amount == Decimal("76.88")
    assert expenses[0].category == "Some category3"
    assert expenses[0].description == "Some description3"
    assert expenses[0].date
    assert expenses[0].id
    assert expenses[0].created_at
    assert expenses[1].user_id == 111
    assert expenses[1].amount == Decimal("24.22")
    assert expenses[1].category == "Some category"
    assert not expenses[1].description
    assert expenses[1].date
    assert expenses[1].id
    assert expenses[1].created_at


@pytest.mark.asyncio
async def test_get_all_expenses_for_nonexistent_user_id(
    expense1,
    expense2,
    expense3,
    expense4,
    expense5,
) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)

    await repo.add(expense1)
    await repo.add(expense2)
    await repo.add(expense3)
    await repo.add(expense4)
    await repo.add(expense5)

    expenses = await repo.get_all(
        user_id=123456789,
        limit=100,
        offset=0,
    )

    assert len(expenses) == 0
    assert not expenses


@pytest.mark.asyncio
async def test_get_expenses_by_category(
    expense1,
    expense2,
    expense3,
    expense4,
    expense5,
) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)

    await repo.add(expense1)
    await repo.add(expense2)
    await repo.add(expense3)
    await repo.add(expense4)
    await repo.add(expense5)

    expenses = await repo.get_by_category(
        user_id=111,
        category="Some category",
    )

    assert len(expenses) == 2
    assert expenses[0].user_id == 111
    assert expenses[0].amount == Decimal("12.34")
    assert expenses[0].category == "Some category"
    assert expenses[0].description == "Some description"
    assert expenses[0].date
    assert expenses[0].created_at
    assert expenses[0].id
    assert expenses[1].user_id == 111
    assert expenses[1].amount == Decimal("24.22")
    assert expenses[1].category == "Some category"
    assert not expenses[1].description
    assert expenses[1].date
    assert expenses[1].id
    assert expenses[1].created_at


@pytest.mark.asyncio
async def test_get_expenses_by_category_no_matches(
    expense1,
    expense2,
    expense3,
    expense4,
    expense5,
) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)

    await repo.add(expense1)
    await repo.add(expense2)
    await repo.add(expense3)
    await repo.add(expense4)
    await repo.add(expense5)

    expenses = await repo.get_by_category(
        user_id=111,
        category="Some nonexistent category",
    )

    assert len(expenses) == 0
    assert not expenses


@pytest.mark.asyncio
async def test_get_expenses_by_date_period(
    expense1_user1,
    expense2_user1,
    expense3_user1,
    expense4_user1,
    expense5_user1,
) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)
    await repo.add(expense1_user1)
    await repo.add(expense2_user1)
    await repo.add(expense3_user1)
    await repo.add(expense4_user1)
    await repo.add(expense5_user1)

    expenses = await repo.get_by_date_period(
        user_id=1,
        start_date=datetime.date(
            year=2025,
            month=6,
            day=1,
        ),
        end_date=datetime.date(
            year=2025,
            month=6,
            day=3,
        ),
    )

    assert len(expenses) == 3
    assert expenses[0].user_id == 1
    assert expenses[0].amount == Decimal("12.34")
    assert expenses[0].category == "Cat1"
    assert not expenses[0].description
    assert expenses[0].date == datetime.date(
        year=2025,
        month=6,
        day=1,
    )
    assert expenses[0].created_at
    assert expenses[0].id
    assert expenses[1].user_id == 1
    assert expenses[1].amount == Decimal("34.56")
    assert expenses[1].category == "Cat2"
    assert not expenses[1].description
    assert expenses[1].date == datetime.date(
        year=2025,
        month=6,
        day=2,
    )
    assert expenses[1].created_at
    assert expenses[1].id
    assert expenses[2].user_id == 1
    assert expenses[2].amount == Decimal("56.78")
    assert expenses[2].category == "Cat2"
    assert not expenses[2].description
    assert expenses[2].date == datetime.date(
        year=2025,
        month=6,
        day=3,
    )
    assert expenses[2].created_at
    assert expenses[2].id

    expenses = await repo.get_by_date_period(
        user_id=1,
        start_date=datetime.date(
            year=2025,
            month=6,
            day=3,
        ),
        end_date=datetime.date(
            year=2025,
            month=6,
            day=11,
        ),
    )

    assert len(expenses) == 1

    expenses = await repo.get_by_date_period(
        user_id=1,
        start_date=datetime.date(
            year=2025,
            month=3,
            day=1,
        ),
        end_date=datetime.date(
            year=2025,
            month=5,
            day=30,
        ),
    )

    assert len(expenses) == 1


@pytest.mark.asyncio
async def test_get_expenses_by_date_period_no_matches(
    expense1_user1,
    expense2_user1,
    expense3_user1,
    expense4_user1,
    expense5_user1,
) -> None:
    _storage: list[Expense] = []
    repo = InMemoryExpenseRepository(_storage)
    await repo.add(expense1_user1)
    await repo.add(expense2_user1)
    await repo.add(expense3_user1)
    await repo.add(expense4_user1)
    await repo.add(expense5_user1)

    expenses = await repo.get_by_date_period(
        user_id=1,
        start_date=datetime.date(
            year=2025,
            month=3,
            day=1,
        ),
        end_date=datetime.date(
            year=2025,
            month=4,
            day=30,
        ),
    )

    assert len(expenses) == 0
    assert not expenses

    expenses = await repo.get_by_date_period(
        user_id=1,
        start_date=datetime.date(
            year=2026,
            month=3,
            day=1,
        ),
        end_date=datetime.date(
            year=2026,
            month=4,
            day=30,
        ),
    )

    assert len(expenses) == 0
    assert not expenses
