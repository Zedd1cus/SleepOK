from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import confirmation_kb_scenario


async def command_reset(message: types.Message):
    await bot.send_message(message.chat.id, "This is reset!", reply_markup=confirmation_kb_scenario)