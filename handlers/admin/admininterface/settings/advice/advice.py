from aiogram import types
from handlers.basehandlers.back import back
from handlers.admin.adminscenario.admin_states_scenario import AdminFSM
from src.create_bot import bot
from aiogram.dispatcher import FSMContext
from keyboards.admin_kb import admin_ui_kb_scenario, \
    admin_advice_interface_kb_scenario, admin_show_interface_kb_scenario, \
    admin_settings_kb_scenario, admin_time_of_advices_kb_scenario
from keyboards.client_kb import five_states_kb_scenario, confirmation_kb_scenario

from database.advice import Advice


dict_of_marks = {'/Плохо': 1,
                 '/Ниже_среднего': 2,
                 '/Средне': 3,
                 '/Выше_среднего': 4,
                 '/Отлично': 5}

save_id = None
save_message = None
save_mark = None
save_time = None


async def get_create_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Введите совет.')


async def get_show_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Советы какого состояния вам показать?',
                           reply_markup=five_states_kb_scenario)


async def get_time_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Выберите промежуток времени для советов.',
                           reply_markup=admin_time_of_advices_kb_scenario)


async def get_delete_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Укажите номер совета, который вы хотите удалить.')


async def get_confirmation_message(message: types.Message):
    await bot.send_message(message.chat.id, 'Вы уверены?', reply_markup=confirmation_kb_scenario)


async def get_method_message(message: types.Message, question: dict):
    await bot.send_message(message.chat.id, question[message.text],
                           reply_markup=five_states_kb_scenario)


async def command_advice(message: types.Message):
    if message.text == '/advice':
        await bot.send_message(message.chat.id, "Это интерфейс советов.",
                               reply_markup=admin_advice_interface_kb_scenario)
        await AdminFSM.advice_interface_state.set()

    elif message.text == '/back':
        await back.command_back(message, admin_ui_kb_scenario)
        await AdminFSM.settings_state.set()


async def command_advice_interface(message: types.Message):
    if message.text == '/show':
        await get_show_message(message)
        await AdminFSM.show_interface_state.set()

    elif message.text == '/back':
        await back.command_back(message, admin_settings_kb_scenario)
        await AdminFSM.advice_state.set()


async def command_mark_interface(message: types.Message):
    global save_mark
    save_mark = message.text[1:]
    await get_time_message(message)
    await AdminFSM.action_interface_state.set()


async def command_time_interface(message: types.Message):
    global save_time
    save_time = message.text[1:]
    await bot.send_message(message.chat.id, f'{save_mark}/{save_time}')
    await bot.send_message(message.chat.id, 'Совет 1')
    await bot.send_message(message.chat.id, 'Совет 2')
    await bot.send_message(message.chat.id, 'Совет 3', reply_markup=admin_show_interface_kb_scenario)
    await AdminFSM.time_interface_state.set()


async def perform_action(message: types.Message):
    if message.text == '/delete':
        await get_delete_message(message)
        await AdminFSM.delete_interface_state.set()

    elif message.text == '/create':
        await get_create_message(message)
        await AdminFSM.create_interface_state.set()

    elif message.text == '/back':
        await back.command_back(message, admin_advice_interface_kb_scenario)
        await AdminFSM.advice_interface_state.set()


async def confirmation_for_delete(message: types.Message):
    global save_id
    save_id = message.text
    await get_confirmation_message(message)
    await AdminFSM.confirmation_for_delete_state.set()


async def delete(message: types.Message):
    """delete advice by id and mark"""
    if message.text == '/Yes':
        await bot.send_message(message.chat.id, f'Вы удалили совет под номером {save_id}')
        await get_show_message(message)
        await AdminFSM.show_interface_state.set()
    elif message.text == '/No':
        await confirmation_for_delete(message)


async def confirmation_for_create(message: types.Message):
    global save_message
    save_message = message.text
    await get_confirmation_message(message)
    await AdminFSM.confirmation_for_create_state.set()


async def create(message: types.Message):
    """create advice by mark"""
    if message.text == '/Yes':
        await bot.send_message(message.chat.id, 'Вы добавили данный совет:\n'
                                                f'{save_message}')
        await get_show_message(message)
        await AdminFSM.show_interface_state.set()
    elif message.text == '/No':
        await confirmation_for_create(message)










def create_advice_by_mark(mark: int, some_advice: str):
    # Advice.create(mark, some_advice)
    pass

def delete_advice_by_mark_and_id(mark: int, id_advice: int):
    pass

def get_advice_by_mark_and_id(mark: int, id_advice: int):
    pass







