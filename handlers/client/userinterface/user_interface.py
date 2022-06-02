from aiogram import types, Dispatcher

from handlers.client.userinterface.help.help import command_help
from handlers.client.userinterface.risedown.rise import command_rise
from handlers.client.userinterface.settings.settings import command_settings
from src.create_bot import bot
from keyboards.client_kb import confirmation_kb_scenario, client_ui_kb_scenario, client_settings_kb_scenario
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from aiogram.dispatcher import FSMContext


async def command_base_ui(tid):
    await bot.send_message(tid, 'Вы находитесь в базовом интерфейсе.',
                           reply_markup=client_ui_kb_scenario)
    await ClientFMS.selection_state.set()


async def command_user_selection(message: types.Message, state:FSMContext):
    if message.text == '/Настройки':
        await command_settings(message)

    elif message.text == '/Подъем':
        await command_rise(message, state)


def base_ui_handlers(dp: Dispatcher):
    dp.register_message_handler(command_base_ui, state=None)
    dp.register_message_handler(command_user_selection,
                                commands=['Подъем', 'Настройки'],
                                state=ClientFMS.selection_state)

