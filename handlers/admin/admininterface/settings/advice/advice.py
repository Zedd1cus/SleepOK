import datetime

from aiogram import types
from handlers.basehandlers.back import back
from handlers.admin.adminscenario.admin_states_scenario import AdminFSM
from src.create_bot import bot
from aiogram.dispatcher import FSMContext
from keyboards.admin_kb import admin_ui_kb_scenario, \
    admin_advice_interface_kb_scenario, admin_show_interface_kb_scenario, \
    admin_settings_kb_scenario, admin_time_of_advices_kb_scenario
from keyboards.client_kb import five_states_kb_scenario, confirmation_kb_scenario
from handlers.client.rоutine.notifications.notification_new import get_state_id
from keyboards.admin_kb import kb_5_11_advices, kb_11_15_advices, kb_20_5_advices, kb_15_20_advices
from database.advice import Advice


dict_of_marks = {1: '"Плохо"',
                 2: '"Ниже среднего"',
                 3: '"Средне"',
                 4: '"Выше среднего"',
                 5: '"Отлично"'}
save_time_for_message = None

keyboards_to_time = [kb_5_11_advices, kb_11_15_advices, kb_20_5_advices, kb_15_20_advices]


async def get_create_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите совет.')


async def get_show_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Советы какого состояния Вам показать?',
                           reply_markup=five_states_kb_scenario)


async def get_time_message(message: types.Message, mark: str):
    await bot.send_message(message.chat.id, f'Выберите промежуток времени для советов {mark}.',
                           reply_markup=admin_time_of_advices_kb_scenario)


async def get_delete_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Укажите номер совета, который Вы хотите удалить.')


async def get_confirmation_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы уверены?', reply_markup=confirmation_kb_scenario)


async def get_method_message(message: types.Message, question: dict):
    await bot.send_message(message.chat.id, question[message.text],
                           reply_markup=five_states_kb_scenario)


async def command_advice(message: types.Message):
    if message.text == '/Советы':
        await bot.send_message(message.chat.id, "Вы находитесь в интерфейсе советов.",
                               reply_markup=admin_advice_interface_kb_scenario)
        await AdminFSM.advice_interface_state.set()

    elif message.text == '/Назад':
        await bot.send_message(message.chat.id, "Вы находитесь в интерфейсе Админа.", reply_markup=admin_ui_kb_scenario)
        await AdminFSM.settings_state.set()


async def command_advice_interface(message: types.Message):
    if message.text == '/Показать':
        await get_show_message(message)
        await AdminFSM.show_interface_state.set()

    elif message.text == '/Назад':
        await bot.send_message(message.chat.id, "Вы находитесь в интерфейсе настроек.",
                               reply_markup=admin_settings_kb_scenario)
        await AdminFSM.advice_state.set()


async def command_mark_interface(message: types.Message, state: FSMContext):
    if message.text == '/Назад':
        await bot.send_message(message.chat.id, "Вы находитесь в интерфейсе советов.",
                               reply_markup=admin_advice_interface_kb_scenario)
        await AdminFSM.advice_interface_state.set()

    else:
        save_mark = get_state_id(message)
        async with state.proxy() as data:
            data['mark'] = save_mark

        await get_time_message(message, dict_of_marks[save_mark])
        await AdminFSM.action_interface_state.set()


async def command_time_interface(message: types.Message, state: FSMContext):
    if message.text == '/Назад':
        await get_show_message(message)
        await AdminFSM.show_interface_state.set()

    else:
        global save_time_for_message
        save_time = None
        save_time_for_message = message.text[1:]
        for keyb in keyboards_to_time:
            if message.text == keyb.text:
                save_time = keyb['hour']
                break
        async with state.proxy() as data:
            save_mark = data['mark']
            data['time'] = save_time
        await bot.send_message(message.chat.id, f'{save_mark}/{save_time}')
        advs = await Advice.get_advices_by_mark_and_hour(save_mark, save_time)
        count = 0
        for adv in advs:
            if count == len(advs):
                await bot.send_message(message.chat.id, reply_markup=admin_show_interface_kb_scenario)
            else:
                await bot.send_message(message.chat.id, adv.advice, reply_markup=admin_show_interface_kb_scenario)
            count += 1
        await AdminFSM.time_interface_state.set()


async def perform_action(message: types.Message, state: FSMContext):
    if message.text == '/Удалить':
        await get_delete_message(message)
        await AdminFSM.delete_interface_state.set()

    elif message.text == '/Создать':
        await get_create_message(message)
        await AdminFSM.create_interface_state.set()

    elif message.text == '/Назад':
        async with state.proxy() as data:
            await get_time_message(message, dict_of_marks[data['mark']])
            await AdminFSM.action_interface_state.set()


async def confirmation_for_delete(message: types.Message, state: FSMContext):
    save_id = message.text
    async with state.proxy() as data:
        data['id'] = save_id
    await get_confirmation_message(message)
    await AdminFSM.confirmation_for_delete_state.set()


async def delete(message: types.Message, state: FSMContext):
    """delete advice by id and mark"""
    if message.text == '/Да':
        async with state.proxy() as data:
            save_id = data['id']
            await bot.send_message(message.chat.id, f'Вы удалили совет под номером "{save_id}"\n'
                                                    f'в {dict_of_marks[data["mark"]]} и "{save_time_for_message}".')
            await get_show_message(message)
            await AdminFSM.show_interface_state.set()
    elif message.text == '/Нет':
        await get_delete_message(message)
        await AdminFSM.delete_interface_state.set()


async def confirmation_for_create(message: types.Message, state: FSMContext):
    save_message = message.text
    async with state.proxy() as data:
        data['message'] = save_message
    await get_confirmation_message(message)
    await AdminFSM.confirmation_for_create_state.set()


async def create(message: types.Message, state: FSMContext):
    """create advice by mark"""
    if message.text == '/Да':
        async with state.proxy() as data:
            save_message = data['message']
            await bot.send_message(message.chat.id, f'Вы добавили данный совет в {dict_of_marks[data["mark"]]} и '
                                                    f'"{save_time_for_message}".')
            await get_show_message(message)
            await AdminFSM.show_interface_state.set()
    elif message.text == '/Нет':
        await get_create_message(message)
        await AdminFSM.create_interface_state.set()


time_arrays = [[i for i in range(5, 11)], [i for i in range(11, 15)], [i for i in range(15, 20)], [i for i in range(20, 5)]]


def create_advice_by_mark(mark: int, some_advice: str):
    hour = datetime.datetime.now().hour
    for arr in time_arrays:
        if hour in arr:
            Advice.create([mark], arr, some_advice)
            break

def delete_advice_by_mark_and_hour(mark: int, id_advice: int):
    Advice.delete_by_uid()

def get_advice_by_mark_and_id(mark: int, id_advice: int):
    Advice.get_advices_by_mark_and_hour()
