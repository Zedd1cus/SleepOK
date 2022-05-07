from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import confirmation_kb_scenario
from keyboards.client_kb import client_ui_kb_scenario
from handlers.client.clientscenario import client_states_scenario
from handlers.basehandlers.back import back
from aiogram.dispatcher import FSMContext


async def command_reset(message: types.Message, state: FSMContext):
    if message.text == '/reset':
        await bot.send_message(message.chat.id, "This is reset!", reply_markup=confirmation_kb_scenario)
        await client_states_scenario.ClientFMS.ui_reset_state.set()
    elif message.text == '/back':
        await back.command_back(message, client_ui_kb_scenario)
        await state.finish()


