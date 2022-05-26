from aiogram import types
from src.create_bot import bot
from aiogram.dispatcher import FSMContext
from handlers.basehandlers.back import back
from handlers.admin.adminscenario import admin_states_scenario
from keyboards.admin_kb import admin_settings_kb_scenario


async def command_settings(message: types.Message, state: FSMContext):
    await bot.send_message(message.chat.id, "This is settings!",
                           reply_markup=admin_settings_kb_scenario)
    await admin_states_scenario.AdminFSM.advice_state.set()
