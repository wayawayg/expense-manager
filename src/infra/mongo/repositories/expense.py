import datetime
from dataclasses import dataclass

from bson.decimal128 import Decimal128
from motor.motor_asyncio import AsyncIOMotorCollection

from src.domain.entities.expense import Expense
from src.infra.mongo.exceptions.expense import DatabaseWriteException


@dataclass
class MongoExpenseRepository:
    _collection: AsyncIOMotorCollection

    @staticmethod
    def _conver_mongo_response_to_entity(data: dict) -> Expense:
        to_convert = data.copy()
        to_convert["amount"] = data["amount"].to_decimal()
        to_convert["date"] = datetime.date(
            year=data["date"].year,
            month=data["date"].month,
            day=data["date"].day,
        )
        return Expense.model_validate(to_convert, from_attributes=True)

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

    async def get_by_category(
        self,
        user_id: int,
        category: str,
    ) -> list[Expense]:
        cursor = self._collection.find(
            {
                "user_id": user_id,
                "category": category,
            }
        )
        result = []
        async for document in cursor:
            expense = self._conver_mongo_response_to_entity(document)
            result.append(expense)
        return result

    async def get_by_date_period(
        self,
        user_id: int,
        start_date: datetime.date,
        end_date: datetime.date,
    ) -> list[Expense]:
        cursor = self._collection.find(
            {
                "user_id": user_id,
                "date": {
                    "$gte": datetime.datetime(
                        year=start_date.year,
                        month=start_date.month,
                        day=start_date.day,
                        tzinfo=datetime.UTC,
                    ),
                    "$lte": datetime.datetime(
                        year=end_date.year,
                        month=end_date.month,
                        day=end_date.day,
                        tzinfo=datetime.UTC,
                    ),
                },
            }
        )
        result = []
        async for document in cursor:
            expense = self._conver_mongo_response_to_entity(document)
            result.append(expense)
        return result
