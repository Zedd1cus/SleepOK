from aiogram import types
from src.create_bot import bot


async def command_help(message: types.Message):
    await bot.send_message(message.chat.id, "This is help!")
    