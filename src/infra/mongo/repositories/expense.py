import datetime
from dataclasses import dataclass

from bson.decimal128 import Decimal128
from motor.motor_asyncio import AsyncIOMotorCollection

from src.domain.entities.expense import Expense
from src.infra.mongo.exceptions.expense import DatabaseWriteException


@dataclass
class MongoExpenseRepository:
    _collection: AsyncIOMotorCollection

    async def add(
        self,
        expense: Expense,
    ) -> str:
        data = expense.model_dump()
        data["amount"] = Decimal128(data["amount"])
        data["date"] = datetime.datetime(
            year=data["date"].year,
            month=data["date"].month,
            day=data["date"].day,
            tzinfo=datetime.UTC,
        )
        insert_result = await self._collection.insert_one(data)
        if not insert_result.inserted_id:
            raise DatabaseWriteException
        return expense.id

    async def get_all(
        self,
        user_id: int,
        limit: int,
        offset: int,
    ) -> list[Expense]:
        expenses = (
            await self._collection.find({"user_id": user_id})
            .skip(offset)
            .to_list(limit)
        )
        result = []
        for expense in expenses:
            expense["amount"] = expense["amount"].to_decimal()
            expense["date"] = datetime.date(
                year=expense["date"].year,
                month=expense["date"].month,
                day=expense["date"].day,
            )
            result.append(Expense.model_validate(expense, from_attributes=True))
        return result
