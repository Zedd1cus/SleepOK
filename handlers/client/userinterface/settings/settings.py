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
    if message.text == '/reset':
        await get_ui_confirmation_message(message)
        await ClientFMS.ui_reset_state.set()
    elif message.text == '/back':
        await user_interface.command_base_ui(message)


async def command_confirmation_reset(message: types.Message):
    if message.text == '/Yes':
        await start_settings.command_rise(message)
    elif message.text == '/No':
        await get_ui_settings_message(message)
        await ClientFMS.ui_settings_state.set()


def user_interface_handlers(dp: Dispatcher):
    # UI Settings
    dp.register_message_handler(command_settings, commands=['settings'],
                                state=None)
    dp.register_message_handler(command_reset, commands=['reset', 'back'],
                                state=ClientFMS.ui_settings_state)

    dp.register_message_handler(command_confirmation_reset, commands=['Yes', 'No'],
                                state=ClientFMS.ui_reset_state)
