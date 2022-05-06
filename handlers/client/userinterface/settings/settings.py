from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import settings_kb_scenario


async def command_settings(message: types.Message):
    await bot.send_message(message.chat.id, "This is settings!", reply_markup=settings_kb_scenario)