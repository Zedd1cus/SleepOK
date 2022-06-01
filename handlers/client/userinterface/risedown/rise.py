from aiogram import types
from database.user import User
from database.state_change import StateChange
from handlers.client.userinterface import user_interface
from keyboards.client_kb import client_ui_kb_scenario, confirmation_kb_scenario
from src.create_bot import bot
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from handlers.client.settings.start_settings import verify_time_of_notification


save_time_of_down = None


async def command_rise(message: types.Message):
    # tid = message.from_user.id
    # user = await User.get(tid)
    # last = await user.get_last_state()
    # is_wake_up = last.state == StateChange.WAKE_UP
    if True:

        await bot.send_message(message.chat.id, "Напишите время, во сколько вы легли.")
        await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')
        await ClientFMS.ui_rise_state.set()

    else:
        await bot.send_message(message.chat.id, "Вы не можете нажать эту кнопку до завтрашнего дня.",
                               reply_markup=client_ui_kb_scenario)
        await ClientFMS.selection_state.set()


async def command_down(message: types.Message):
    global save_time_of_down
    if len(message.text) == 4:
        save_time_of_down = '0' + message.text
    else:
        save_time_of_down = message.text

    if verify_time_of_notification(save_time_of_down):
        await bot.send_message(message.chat.id, f"Вы увeрены, что легли в {save_time_of_down}?",
                               reply_markup=confirmation_kb_scenario)
        await ClientFMS.ui_down_state.set()

    else:
        await bot.send_message(message.chat.id, 'Введен неверный формат!')
        await command_rise(message)


async def command_confirmation(message: types.Message):
    if message.text == '/Yes':
        await user_interface.command_base_ui(message.chat.id)

    elif message.text == '/No':
        await command_rise(message)







