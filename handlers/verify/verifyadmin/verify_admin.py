from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import admin_kb_scenario


async def command_verify_admin(message: types.Message):
    await bot.send_message(message.chat.id, "This is client!", reply_markup=admin_kb_scenario)