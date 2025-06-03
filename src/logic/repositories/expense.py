from dataclasses import dataclass
from datetime import date
from typing import Any, Protocol

from src.domain.entities.expense import Expense


class ExpenseRepository(Protocol):
    async def add(
        self,
        expense: Expense,
    ) -> Expense:
        raise NotImplementedError

    async def get_all(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list[Expense]:
        raise NotImplementedError

    async def get_by_category(
        self,
        user_id: int,
        category: str,
    ) -> list[Expense]:
        raise NotImplementedError

    async def get_by_date_period(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> list[Expense]:
        raise NotImplementedError


@dataclass
class InMemoryExpenseRepository:
    _storage: list[Expense]

    async def add(
        self,
        expense: Expense,
    ) -> Expense:
        self._storage.append(expense)
        return expense

    async def get_all(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list[Expense]:
        result = []
        for expense in self._storage:
            if expense.user_id == user_id:
                result.append(expense)
        return result[offset : offset + limit]

    async def get_by_category(
        self,
        user_id: int,
        category: str,
    ) -> list[Expense]:
        result = []
        for expense in self._storage:
            if expense.user_id == user_id and expense.category == category:
                result.append(expense)
        return result

    async def get_by_date_period(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> list[Expense]:
        result = []
        for expense in self._storage:
            if (
                expense.user_id == user_id
                and expense.date
                and expense.date >= start_date
                and expense.date <= end_date
            ):
                result.append(expense)
        return result
