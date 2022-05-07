from aiogram import types
from src.create_bot import bot
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import client_ui_kb_scenario


async def command_confirmation(message: types.Message, state: FSMContext):
    if message.text == "/Yes":
        await bot.send_message(message.chat.id, "What do you want to change?")
        await state.finish()

    elif message.text == "/No":
        await bot.send_message(message.chat.id, "This is No!", reply_markup=client_ui_kb_scenario)
        await state.finish()

