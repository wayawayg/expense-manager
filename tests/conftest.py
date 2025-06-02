import pytest_asyncio

from src.infra.mongo.config import expense_collection


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clean_collections():
    yield

    await expense_collection.delete_many({})
