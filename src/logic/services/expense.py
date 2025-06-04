from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from src.domain.entities.expense import Expense
from src.logic.repositories.expense import ExpenseRepository


@dataclass(eq=False, slots=True)
class ExpenseService:
    repository: ExpenseRepository

    def create_new_expense(
        self,
        user_id: int,
        amount: Decimal,
        category: str,
        date: date | None = None,
        description: str | None = None,
    ) -> Expense:
        expense = Expense(
            user_id=user_id,
            amount=amount,
            category=category,
            description=description,
            date=date,
        )
        self.repository.add(expense)
        return expense

    def get_expenses(
        self,
        user_id: int,
        limit: int = 100,
        offset: int = 0,
    ) -> list[Expense]:
        expenses = self.repository.get_all(user_id, limit, offset)
        return expenses

    def get_expenses_by_category(
        self,
        user_id: int,
        category: str,
    ) -> list[Expense]:
        expenses = self.repository.get_by_category(user_id, category)
        return expenses

    def get_expenses_by_date_period(
        self,
        user_id: int,
        start_date: date,
        end_date: date,
    ) -> list[Expense]:
        expenses = self.repository.get_by_date_period(
            user_id,
            start_date,
            end_date,
        )
        return expenses
