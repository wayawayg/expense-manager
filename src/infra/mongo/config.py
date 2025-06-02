from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorCollection,
    AsyncIOMotorDatabase,
)

from src.common.config import config

client: AsyncIOMotorClient = AsyncIOMotorClient(config.mongo.url)

database: AsyncIOMotorDatabase = client.get_database(config.mongo.database)
expense_collection: AsyncIOMotorCollection = database[config.mongo.expense_collection]
