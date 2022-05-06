from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import ui_kb_scenario


async def command_confirmation(message: types.Message):
    if message.text == "/Yes":
        await bot.send_message(message.chat.id, "What do you want to change?")

    elif message.text == "/No":
        await bot.send_message(message.chat.id, "This is No!", reply_markup=ui_kb_scenario)