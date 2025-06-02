import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(eq=False, frozen=True)
class Mongo:
    url: str = os.environ["MONGO_URL"]
    database: str = os.environ["MONGO_DATABASE_NAME"]
    expense_collection: str = os.environ["MONGO_EXPENSE_COLLECTION_NAME"]


@dataclass(eq=False, frozen=True)
class Telegram:
    token: str = os.environ["TELEGRAM_BOT_TOKEN"]


@dataclass(eq=False, frozen=True)
class Config:
    mongo: Mongo = Mongo()
    telegram: Telegram = Telegram()


config = Config()
