from aiogram import types
from src.create_bot import bot
from aiogram.dispatcher.filters.state import State, StatesGroup
from keyboards.admin_kb import admin_ui_kb_scenario


class AdminFSM(StatesGroup):
    settings_state = State()
    advice_state = State()

    advice_interface_state = State()
    show_interface_state = State()
    time_interface_state = State()

    action_interface_state = State()

    confirmation_for_delete_state = State()
    confirmation_for_create_state = State()

    delete_interface_state = State()
    create_interface_state = State()


async def command_admin(message: types.Message):
    if message.from_user.id == 653694622: # if message.from_user.id == admin_user:
        await bot.send_message(message.chat.id, "Вы находитесь в интерфейсе админа.", reply_markup=admin_ui_kb_scenario)
        await AdminFSM.settings_state.set()

