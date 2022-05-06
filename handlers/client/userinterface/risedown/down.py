from aiogram import types
from src.create_bot import bot


async def command_down(message: types.Message):
    await bot.send_message(message.chat.id, "This is down!")
    