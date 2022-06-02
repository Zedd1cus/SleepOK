import re
import datetime
import asyncio
from aiogram.dispatcher import FSMContext
from aiogram import types

from handlers.client.rоutine.notifications.notification_new import handle_player
from handlers.client.userinterface import user_interface
from src.create_bot import bot
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from keyboards.client_kb import confirmation_kb_scenario

from database.user import User

time_of_rise = None
time_of_sleep = None
array_of_time_of_notification = None


def verify_time_of_notification(time: str) -> bool:
    regex = "^(([01]?[0-9])|([01][0-9])|2[0-3]):[0-5][0-9]$"
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
    if message.from_user.id != 653694622:
        await get_rise_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_rise.set()
    else:
        print('Админу нельзя')


async def command_set_up_rise(message: types.Message):
    global time_of_rise
    if len(message.text) == 4:
        time_of_rise = '0' + message.text
    else:
        time_of_rise = message.text
    if verify_time_of_notification(time_of_rise):
        await get_confirmation_message(message, time_of_rise, 'rise')
        await ClientFMS.settings_set_up_rise.set()
    else:
        await get_wrong_message(message)
        await get_rise_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_rise.set()


async def command_confirmation_rise(message: types.Message, state: FSMContext):
    global time_of_rise
    if message.text == '/Да':
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
    if len(message.text) == 4:
        time_of_sleep = '0' + message.text
    else:
        time_of_sleep = message.text
    if verify_time_of_notification(time_of_sleep):
        await get_confirmation_message(message, time_of_sleep, 'sleep')
        await ClientFMS.settings_set_up_sleep.set()
    else:
        await get_wrong_message(message)
        await get_sleep_message(message)
        await get_format_time_message(message)
        await ClientFMS.settings_confirmation_rise.set()


async def command_confirmation_sleep(message: types.Message, state: FSMContext):
    global time_of_sleep
    if message.text == '/Да':
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
            if len(time) == 5:
                string_of_time_of_notification += time + '\n'
            else:
                string_of_time_of_notification += '0' + time + '\n'
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
    if message.text == '/Да':
        #await connect.init()
        user = await User.get(message.from_user.id) # само же создает юзера в бд

        async with state.proxy() as data:
            data['array_of_time_of_notification'] = array_of_time_of_notification
            await user.set_time_to_up(datetime.time.fromisoformat(data['time_of_rise']))
            await user.set_time_to_sleep(datetime.time.fromisoformat(data['time_of_sleep']))
            await user.set_notification_time([datetime.time.fromisoformat(k) for k in data['array_of_time_of_notification']])
        asyncio.create_task(handle_player(user.tid))
        await user_interface.command_base_ui(message.chat.id)
    else:
        await get_time_of_notification_message(message)
        await ClientFMS.settings_confirmation_sleep.set()