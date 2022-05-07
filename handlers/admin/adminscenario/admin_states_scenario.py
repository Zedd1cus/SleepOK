from aiogram import types
from src.create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.client_kb import admin_ui_kb_scenario


class AdminFSM(StatesGroup):
    settings_state = State()
    advice_state = State()


async def command_admin(message: types.Message):
    await bot.send_message(message.chat.id, "This is admin!", reply_markup=admin_ui_kb_scenario)
    await AdminFSM.settings_state.set()

