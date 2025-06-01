import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(eq=False, frozen=True)
class Telegram:
    token: str = os.environ["TELEGRAM_BOT_TOKEN"]


@dataclass(eq=False, frozen=True)
class Config:
    telegram: Telegram = Telegram()


config = Config()
