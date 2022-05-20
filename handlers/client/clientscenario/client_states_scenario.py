from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from src.create_bot import bot
from aiogram.dispatcher import FSMContext

from keyboards.client_kb import client_ui_kb_scenario


class ClientFMS(StatesGroup):
    # Base UI
    selection_state = State()

    # UI Settings
    ui_settings_state = State()
    ui_reset_state = State()


    # # UI Help
    # ui_help_state = State()

    # # UI Rise or down
    # ui_rise_state = State()
    # ui_down_state = State()

    # Start settings
    settings_rise = State()
    settings_set_up_rise = State()
    settings_confirmation_rise = State()

    settings_sleep = State()
    settings_set_up_sleep = State()
    settings_confirmation_sleep = State()

    settings_time_of_notification = State()
    settings_set_up_time_of_notification = State()
    settings_confirmation_time_of_notification = State()



