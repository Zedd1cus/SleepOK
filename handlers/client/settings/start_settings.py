from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import confirmation_kb_scenario, client_ui_kb_scenario


class NotificationFSM(StatesGroup):
    get_up = State()  # состояние ввода времени подъёма
    yes_no_1 = State()  # кнопки да/нет для подтверждения предыдущего состояния
    sleep = State()  # состояние ввода времени сна
    yes_no_2 = State()  # кнопки да/нет для подтверждения предыдущего состояния
    notifications = State()  # состояние ввода времени уведомления
    yes_no_3 = State()  # кнопки да/нет для подтверждения предыдущего состояния
    end = State()  # конец


# @dp.message_handler(commands=['start', 'help'], state=None)
async def send_welcome(message: types.Message):
    await NotificationFSM.get_up.set()
    await bot.send_message(message.chat.id, "Привет! Я бот, который поможет тебе улучшить качество сна.")
    await bot.send_message(message.chat.id, "Напишите время, когда вы хотите вставать.")
    await time_rule(message)


async def time_rule(message):
    await bot.send_message(message.from_user.id, 'Формат: "часы:минуты".')


hours_1 = None  # переменная, в которую записываются часы пробуждения
minutes_1 = None  # переменная, в которую записываются минуты пробуждения
hours_2 = None  # переменная, в которую записываются часы начала сна
minutes_2 = None  # переменная, в которую записываются минуты начала сна
array_of_time_notify = []  # список, в который добавляем времена уведомлений



# @dp.message_handler(state=NotificationFSM.get_up)
async def first_data(message: types.Message):
    global hours_1
    global minutes_1
    s_mes = message.text.split(':')
    if len(s_mes) == 2:
        try:
            hours_1 = (s_mes[0])
            minutes_1 = (s_mes[1])
            if (24 >= int(hours_1) >= 0) and (60 > int(minutes_1) >= 0):
                await NotificationFSM.yes_no_1.set()
                await bot.send_message(message.from_user.id, f"Вы хотите вставать в {hours_1}:{minutes_1}?",
                                       reply_markup=confirmation_kb_scenario)

            else:
                raise ValueError

        except Exception:
            hours_1 = None
            minutes_1 = None
            await bot.send_message(message.chat.id, "Введен неверный формат!")
            await time_rule(message)

    else:
        await bot.send_message(message.chat.id, "Введен неверный формат!")
        await time_rule(message)


async def f_yes_1(message):
    # async with state.proxy() as data:
    # data['hours'] = hours_1 # вот тут изначально планировалось записать данные в само состояние, но возникает какая-то ошибка
    # data['minutes'] = minutes_1
    await NotificationFSM.sleep.set()
    await bot.send_message(message.from_user.id, "Напишите время, когда вы хотите ложиться спать.")
    await time_rule(message)

# @dp.message_handler(state=NotificationFSM.yes_no_1)
async def f_yes_no_1(message: types.Message):
    if message.text == '/Yes':
        await NotificationFSM.get_up.set()
        await f_yes_1(message)
    else:
        await NotificationFSM.get_up.set()
        await time_rule(message)


# @dp.register_message_handler(state=NotificationFSM.sleep)
async def second_data(message):
    global hours_2
    global minutes_2
    s_mes = message.text.split(':')
    if len(s_mes) == 2:
        try:
            hours_2 = s_mes[0]
            minutes_2 = s_mes[1]
            if (24 >= int(hours_2) >= 0) and (60 > int(minutes_2) >= 0):
                await NotificationFSM.yes_no_2.set()
                await bot.send_message(message.chat.id, f"вы хотите ложиться в {hours_2}:{minutes_2}?",
                                       reply_markup=confirmation_kb_scenario)

            else:
                raise ValueError

        except Exception:
            hours_2 = None
            minutes_2 = None
            await bot.send_message(message.chat.id, "Введен неверный формат!")
            await time_rule(message)

    else:
        await bot.send_message(message.chat.id, "Введен неверный формат!")
        await time_rule(message)


# @dp.message_handler(state=NotificationFSM.yes_no_2)
async def f_yes_no_2(message: types.Message):
    if message.text == '/Yes':
        await NotificationFSM.sleep.set()
        await f_yes_2(message)
    else:
        await NotificationFSM.sleep.set()
        await time_rule(message)


async def f_yes_2(message):
    await NotificationFSM.notifications.set()
    await notif_rule(message)


async def notif_rule(message):
    await bot.send_message(message.from_user.id,
                           'Пожалуйста, введите время уведомлений для оценки состояния.\n'
                           'Вводите в том же формате:\n'
                           '"часы:минуты"\n'
                           '"часы:минуты"\n'
                           '...............................\n'
                           '"часы:минуты"')


# @dp.register_message_handler(state=NotificationFSM.notifications)
async def notifications_data(message):
    global array_of_time_notify
    string_of_time_notify = ''
    array_of_time_notify = message.text.split()
    for i in array_of_time_notify:
        if verify_time_data(i):
            string_of_time_notify += i + '\n'

        else:
            array_of_time_notify.clear()
            await bot.send_message(message.chat.id, "Введен неверный формат!")
            await notif_rule(message)
            await NotificationFSM.notifications.set()
            return

    await bot.send_message(message.chat.id, "Вы хотите получать уведомления в\n"
                                            f"{string_of_time_notify[:-1]}?", reply_markup=confirmation_kb_scenario)
    await NotificationFSM.yes_no_3.set()


def verify_time_data(time_notify):
    s_mes = time_notify.split(':')

    if len(s_mes) == 2:
        hours = int(s_mes[0])
        minutes = int(s_mes[1])
        if (24 >= hours >= 0) and (60 > minutes >= 0):
            return True
        else:
            return False
    else:
        return False


# @dp.message_handler(state=NotificationFSM.yes_no_3)
async def f_yes_no_3(message: types.Message, state=FSMContext):
    global array_of_time_notify
    if message.text == '/Yes':
        await bot.send_message(message.chat.id, 'Спасибо за введенные данные!', reply_markup=client_ui_kb_scenario)
        await state.finish()

    else:
        array_of_time_notify.clear()
        await notif_rule(message)
        await NotificationFSM.notifications.set()
