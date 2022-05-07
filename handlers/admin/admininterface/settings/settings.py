from aiogram import types
from src.create_bot import bot
from aiogram.dispatcher import FSMContext
from handlers.basehandlers.back import back
from handlers.admin.adminscenario import admin_states_scenario
from keyboards.client_kb import admin_settings_kb_scenario, verify_kb_scenario


async def command_settings(message: types.Message, state: FSMContext):
    if message.text == '/settings':
        await bot.send_message(message.chat.id, "This is admin interface!",
                               reply_markup=admin_settings_kb_scenario)
        await admin_states_scenario.AdminFSM.advice_state.set()
    elif message.text == '/back':
        await back.command_back(message, verify_kb_scenario)
        await state.finish()
