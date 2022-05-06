from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import ui_kb_scenario


async def command_verify_client(message: types.Message):
    await bot.send_message(message.chat.id, "This is client!", reply_markup=ui_kb_scenario)
