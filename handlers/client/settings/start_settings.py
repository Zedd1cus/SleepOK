import re
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types

from handlers.client.userinterface import user_interface
from src.create_bot import bot
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from keyboards.client_kb import confirmation_kb_scenario, client_ui_kb_scenario
from aiogram import Dispatcher


time_of_rise = None
time_of_sleep = None
array_of_time_of_notification = None


def verify_time_of_notification(time: str) -> bool:
    regex = "^([01]?[0-9]|2[0-3]):[0-5][0-9]$"
    p = re.compile(regex)
    if time == "":
        return False
    m = re.search(p, time)
    if m is None:
        return False
    else:
        return True


async def get_confirmation_message(message: types.Message, time: str, rise_or_sleep: str):
    if rise_or_sleep == 'rise':
        await bot.send_message(message.chat.id, f'Вы хотите вставать в {time}?', reply_markup=confirmation_kb_scenario)
    elif rise_or_sleep == 'sleep':
        await bot.send_message(message.chat.id, f'Вы хотите ложиться в {time}?', reply_markup=confirmation_kb_scenario)


async def get_format_time_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')


async def get_wrong_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Введен неверный формат!')


async def get_rise_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Укажите время, в которое вы хотите вставать.')


async def get_sleep_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Укажите время, в которое вы хотите ложиться.')


async def get_time_of_notification_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Пожалуйста, введите время уведомлений для оценки состояния.\n'
                                            'Формат:\n'
                                            '"часы:минуты"\n'
                                            '"часы:минуты"\n'
                                            '..............................\n'
                                            '"часы:минуты"')

async def get_verify_time_of_notification_message(message: types.Message, row_of_time: str):
    await bot.send_message(message.chat.id, "Вы хотите получать уведомления в\n"
                                            f"{row_of_time[:-1]}?", reply_markup=confirmation_kb_scenario)


async def command_rise(message: types.Message):
    await get_rise_message(message)
    await get_format_time_message(message)
    await ClientFMS.settings_rise.set()


async def command_set_up_rise(message: types.Message):
    global time_of_rise
    time_of_rise = message.text
    if verify_time_of_notification(message.text):
        await get_confirmation_message(message, message.text, 'rise')
        await ClientFMS.settings_set_up_rise.set()
    else:
        await get_wrong_message(message)
        await get_rise_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_rise.set()


async def command_confirmation_rise(message: types.Message, state: FSMContext):
    global time_of_rise
    if message.text == '/Yes':
        async with state.proxy() as data:
            data['time_of_rise'] = time_of_rise
        await get_sleep_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_confirmation_rise.set()
    else:
        await get_rise_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_rise.set()


async def command_set_up_sleep(message: types.Message):
    global time_of_sleep
    time_of_sleep = message.text
    if verify_time_of_notification(message.text):
        await get_confirmation_message(message, message.text, 'sleep')
        await ClientFMS.settings_set_up_sleep.set()
    else:
        await get_wrong_message(message)
        await get_sleep_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_confirmation_rise.set()


async def command_confirmation_sleep(message: types.Message, state: FSMContext):
    global time_of_sleep
    if message.text == '/Yes':
        async with state.proxy() as data:
            data['time_of_sleep'] = time_of_sleep
        await get_time_of_notification_message(message)
        await ClientFMS.settings_confirmation_sleep.set()
    else:
        await get_sleep_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_confirmation_rise.set()


async def command_set_up_time_of_notification(message: types.Message):
    global array_of_time_of_notification
    array_of_time_of_notification = message.text.splitlines()
    string_of_time_of_notification = ''
    flag = True

    for time in array_of_time_of_notification:
        if verify_time_of_notification(time):
            string_of_time_of_notification += time + '\n'
        else:
            flag = False
            break

    if flag:
        await get_verify_time_of_notification_message(message, string_of_time_of_notification)
        await ClientFMS.settings_set_up_time_of_notification.set()
    else:
        await get_wrong_message(message)
        await get_time_of_notification_message(message)
        await ClientFMS.settings_confirmation_sleep.set()


async def command_confirmation_time_of_notification(message: types.Message, state: FSMContext):
    global array_of_time_of_notification
    if message.text == '/Yes':
        async with state.proxy() as data:
            data['array_of_time_of_notification'] = array_of_time_of_notification
        await user_interface.command_base_ui(message)
    else:
        await get_time_of_notification_message(message)
        await ClientFMS.settings_confirmation_sleep.set()
