from aiogram import types
from handlers.basehandlers.back import back
from handlers.admin.adminscenario import admin_states_scenario
from src.create_bot import bot
from aiogram.dispatcher import FSMContext
from keyboards.client_kb import admin_ui_kb_scenario


async def command_advice(message: types.Message, state: FSMContext):
    if message.text == '/advice':
        await bot.send_message(message.chat.id, "This is advice!")
        await state.finish()
    elif message.text == '/back':
        await back.command_back(message, admin_ui_kb_scenario)
        await admin_states_scenario.AdminFSM.settings_state.set()
