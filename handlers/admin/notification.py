from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import kb_client


class NotificationFSM(StatesGroup):
    state_1 = State()
    state_2 = State()
    state_3 = State()


number_of_notification = None
array_of_time = []


# Функция, которая проверяет, хранится ли в переменной number хоть какое-то значение
def number_is_empty(number: (None, str)) -> bool:
    if number is None:
        return True
    else:
        return False


def array_is_empty(array: list) -> bool:
    if len(array) == 0:
        return True
    else:
        return False


# Функция, которая ловит команду /notification
async def command_notification_start(message: types.Message):


    # Если число пустое, то условие следует первому сценарию
    if number_is_empty(number_of_notification) and array_is_empty(array_of_time):
        await bot.send_message(message.chat.id, 'Укажите количество уведомлений для трекера состояний:')
        # Помечаем состояние state_1 в классе NotificationFSM
        await NotificationFSM.state_1.set()


    # Если не пустое, то вступает в силу 2 сценарий

    elif not number_is_empty(number_of_notification) and not array_is_empty(array_of_time):
        await bot.send_message(message.chat.id, f'Число уведомлений: {number_of_notification}\n'
                                                f'Время для трекера состояний: {array_of_time}')
        await bot.send_message(message.chat.id, 'Хочешь поменять?')
        # Помечаем состояние state_1 в классе NotificationFSM
        await NotificationFSM.state_1.set()


    elif not number_is_empty(number_of_notification) and array_is_empty(array_of_time):
        await bot.send_message(message.chat.id, f'Число уведомлений: {number_of_notification}')
        await bot.send_message(message.chat.id, 'Хочешь поменять?')
        # Помечаем состояние state_1 в классе NotificationFSM
        await NotificationFSM.state_1.set()


# Ловим первый ответ
async def set_state_1(message: types.Message, state: FSMContext):
    global number_of_notification
    global array_of_time
    # Если number не пустое и пользователь ввел 'Да', то делаем number пустым
    if not number_is_empty(number_of_notification) and message.text == 'Да':
        number_of_notification = None
        array_of_time.clear()
        # Возвращаемся в функцию выше и следуем первому сценарию
        await command_notification_start(message)

    elif number_is_empty(number_of_notification) and array_is_empty(array_of_time) and message.text.isdigit():
        number_of_notification = message.text

        if number_of_notification == 1:
            await bot.send_message(message.chat.id, f'Укажите время для {number_of_notification} уведомления:\n'
                                                    f'(Пишите через проблем в формате часы:минуты)')
            # Переходим в состояние state_2
            await NotificationFSM.next()
        else:
            await bot.send_message(message.chat.id, f'Укажите время для {number_of_notification} уведомлений:\n'
                                                    f'(Пишите через пробел в формате часы:минуты)')
            # Переходим в состояние state_2
            await NotificationFSM.next()

    elif not number_is_empty(number_of_notification) and \
            not array_is_empty(array_of_time) and message.text == 'Нет':
        await bot.send_message(message.chat.id, 'Нет, так нет...', reply_markup=kb_client)

    else:
        await bot.send_message(message.chat.id, 'Ошибка, попробуй снова...')
        await command_notification_start(message)


# Ловим второй ответ(функция будет переделана)
async def set_state_2(message: types.Message, state: FSMContext):
    time_of_number = message.text.split()
    global number_of_notification
    global array_of_time
    count = 0

    for i in time_of_number:
        # Добавляем время в массив array_of_time если удовлетворяет условию времени
        if verify_time(i):
            array_of_time.append(i)

        else:
            count += 1

    else:
        if count != 0:
            await bot.send_message(message.chat.id, 'Ошибка, попробуй снова...')
            number_of_notification = None
            array_of_time.clear()
            await command_notification_start(message)

        else:
            await bot.send_message(message.chat.id, "Ты уверен в том, что выбрал?")
            # Переходим в состояние state_3
            await NotificationFSM.next()


# Проверка времени(в дальнейшем дополнится всеми остальными проверками и исключениями)
def verify_time(time: str) -> bool:
    if len(time) == 5 and time[2] == ':':
        return True
    else:
        return False


# Ловим третий ответ
async def set_state_3(message: types.Message, state: FSMContext):
    global number_of_notification
    global array_of_time

    if message.text == 'Да':
        await bot.send_message(message.chat.id, f'{number_of_notification} - number_of_notification\n'
                                                f'{array_of_time} - array_of_time')
        # Завершение машины состояний
        await state.finish()

    elif message.text == 'Нет':
        number_of_notification = None
        array_of_time.clear()
        await command_notification_start(message)
