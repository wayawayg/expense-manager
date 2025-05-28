from dataclasses import dataclass
from typing import Any, Protocol

from src.domain.entities.expense import Expense


class ExpenseRepository(Protocol):
    def add(
        self,
        expense: Expense,
    ) -> Expense:
        raise NotImplementedError

    def get_all(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list[Expense]:
        raise NotImplementedError


@dataclass
class InMemoryExpenseRepository:
    _storage: list[Expense]

    def add(
        self,
        expense: Expense,
    ) -> Expense:
        self._storage.append(expense)
        return expense

    def get_all(
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
