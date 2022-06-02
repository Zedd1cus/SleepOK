from aiogram import types, Dispatcher

from src.create_bot import bot
from keyboards.client_kb import confirmation_kb_scenario, client_settings_kb_scenario
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from aiogram.dispatcher import FSMContext
from handlers.client.settings import start_settings
from handlers.client.userinterface import user_interface


async def get_ui_settings_message(message: types.Message):
    await bot.send_message(message.from_user.id, "Вы находитесь в интерфейсе настроек.",
                           reply_markup=client_settings_kb_scenario)


async def get_ui_confirmation_message(message: types.Message):
    await bot.send_message(message.from_user.id, 'Вы уверены в этом?', reply_markup=confirmation_kb_scenario)


async def command_settings(message: types.Message):
    await get_ui_settings_message(message)
    await ClientFMS.ui_settings_state.set()


async def command_reset(message: types.Message, state: FSMContext):
    if message.text == '/Сброс':
        await get_ui_confirmation_message(message)
        await ClientFMS.ui_reset_state.set()
    elif message.text == '/Назад':
        await user_interface.command_base_ui(message.chat.id)


async def command_confirmation_reset(message: types.Message):
    if message.text == '/Да':
        await start_settings.command_rise(message)
    elif message.text == '/Нет':
        await get_ui_settings_message(message)
        await ClientFMS.ui_settings_state.set()


def user_interface_handlers(dp: Dispatcher):
    # UI Settings
    dp.register_message_handler(command_settings, commands=['Настройка'],
                                state=None)
    dp.register_message_handler(command_reset, commands=['Сброс', 'Назад'],
                                state=ClientFMS.ui_settings_state)

    dp.register_message_handler(command_confirmation_reset, commands=['Да', 'Нет'],
                                state=ClientFMS.ui_reset_state)
