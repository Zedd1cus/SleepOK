from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import verify_kb_scenario


async def command_start(message: types.Message):
    await bot.send_message(message.chat.id, "What's up!", reply_markup=verify_kb_scenario)
