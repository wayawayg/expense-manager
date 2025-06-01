import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from src.common.config import config
from src.common.logger import configure_logger
from src.delivery.telegram.handlers.start import start_router


async def main():
    configure_logger(level=logging.INFO)

    bot = Bot(
        token=config.telegram.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()

    dispatcher.include_router(start_router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
