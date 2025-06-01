from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer("Privet, ya Vitya")
