import asyncio
from create_bot import TelegramBotManager, Logger
from handlers.start import start_router

async def main():
    logger = Logger()
    tg = TelegramBotManager()
    tg.dp.include_router(start_router)
    await tg.dp.start_polling(tg.bot)

if __name__ == "__main__":
    asyncio.run(main())