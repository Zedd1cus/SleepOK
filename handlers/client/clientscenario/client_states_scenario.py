from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from src.create_bot import bot
from aiogram.dispatcher import FSMContext

from keyboards.client_kb import client_ui_kb_scenario, client_settings_kb_scenario


class ClientFMS(StatesGroup):
    # UI Settings
    ui_settings_state = State()
    ui_reset_state = State()

    # UI Help
    ui_help_state = State()

    # UI Rise or down
    ui_rise_state = State()
    ui_down_state = State()


async def command_client(message: types.Message):
    await bot.send_message(message.chat.id, "This is client!", reply_markup=client_ui_kb_scenario)

