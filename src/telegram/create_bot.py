import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
import os
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv(os.path.join(os.path.dirname(__file__), "../../.env"))

@dataclass
class TelegramConfg:
    bot_token: str = os.getenv("BOT_TOKEN")


@dataclass
class TelegramBotManager:
    bot: Bot = Bot(token=TelegramConfg.bot_token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp: Dispatcher = Dispatcher()
    

@dataclass
class Logger:
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    logger = logging.getLogger(__name__)
