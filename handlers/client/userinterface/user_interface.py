from aiogram import types, Dispatcher

from handlers.client.userinterface.help.help import command_help
from handlers.client.userinterface.risedown.rise import command_rise
from handlers.client.userinterface.risedown.down import command_down
from handlers.client.userinterface.settings.settings import command_settings
from src.create_bot import bot
from keyboards.client_kb import confirmation_kb_scenario, client_ui_kb_scenario, client_settings_kb_scenario
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from handlers.client.settings import start_settings


async def command_base_ui(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы находитесь в базовом интерфейсе.',
                           reply_markup=client_ui_kb_scenario)
    await ClientFMS.selection_state.set()


async def command_user_selection(message: types.Message):
    if message.text == '/help':
        await command_help(message)

    elif message.text == '/settings':
        await command_settings(message)

    elif message.text == '/rise':
        await command_rise(message)

    elif message.text == '/down':
        await command_down(message)


def base_ui_handlers(dp: Dispatcher):
    dp.register_message_handler(command_base_ui, state=None)
    dp.register_message_handler(command_user_selection,
                                commands=['help', 'rise', 'down', 'settings'],
                                state=ClientFMS.selection_state)

