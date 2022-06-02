import datetime
from aiogram.dispatcher import FSMContext
from aiogram import types
from database.user import User
from database.state_change import StateChange
from handlers.client.rоutine.graphs import graphs
from handlers.client.userinterface import user_interface
from keyboards.client_kb import client_ui_kb_scenario, confirmation_kb_scenario
from src.create_bot import bot
from handlers.client.clientscenario.client_states_scenario import ClientFMS
from handlers.client.settings.start_settings import verify_time_of_notification


save_time_of_down = None


async def command_rise(message: types.Message, state: FSMContext):
    tid = message.from_user.id
    user = await User.get(tid)
    last = await user.get_last_state()
    # is_wake_up = last.state == StateChange.WAKE_UP
    now_time = datetime.datetime.now()
    if last is None or last.timestamp.day != now_time.day:
        async with state.proxy() as data:
            data['rise'] = now_time
        await bot.send_message(message.chat.id, "Вы встали сейчас?", reply_markup=confirmation_kb_scenario)
        # await bot.send_message(message.chat.id, "Ок, вы встали, а теперь, пожалуйста...")
        # await bot.send_message(message.chat.id, "Напишите время, во сколько вы легли.")
        # await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')
        # await ClientFMS.ui_rise_state.set()
        await ClientFMS.rise_agree.set()
    else:
        await bot.send_message(message.chat.id, "Вы не можете использовать эту кнопку до завтрашнего дня.",
                               reply_markup=client_ui_kb_scenario)
        await ClientFMS.selection_state.set()

async def rise_agree(message: types.Message, state: FSMContext):
    if message.text == '/Да':
        await bot.send_message(message.chat.id, "А теперь напишите время, во сколько Вы легли.")
        await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')
        await ClientFMS.ui_rise_state.set()
    elif message.text == '/Нет':
        await bot.send_message(message.chat.id, "Напишите время, во сколько Вы встали.")
        await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')
        await ClientFMS.rise_changed.set()

async def rise_changed(message: types.Message, state: FSMContext):
    if len(message.text) == 4:
        save_time_of_rise = '0' + message.text
    else:
        save_time_of_rise = message.text
    async with state.proxy() as data:
        data['rise'] = datetime.datetime.today().replace(hour=int(save_time_of_rise[:2]), minute=int(save_time_of_rise[3:]))
    if verify_time_of_notification(save_time_of_rise):
        await bot.send_message(message.chat.id, f"Вы увeрены, что встали в {save_time_of_rise}?",
                               reply_markup=confirmation_kb_scenario)
        await ClientFMS.rise_changed_agree.set()
    else:
        await bot.send_message(message.chat.id, 'Введен неверный формат!')
        await command_rise(message, state)

async def rise_changed_agree(message: types.Message, state: FSMContext):
    if message.text == '/Да':
        await bot.send_message(message.chat.id, "А теперь напишите время, во сколько Вы легли.")
        await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')
        await ClientFMS.ui_rise_state.set()
    elif message.text == '/Нет':
        await rise_agree(message, state)


async def command_down(message: types.Message, state: FSMContext):
    if len(message.text) == 4:
        save_time_of_down = '0' + message.text
    else:
        save_time_of_down = message.text
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    async with state.proxy() as data:
        data['down'] = yesterday.replace(hour=int(save_time_of_down[:2]), minute=int(save_time_of_down[3:]))
    if verify_time_of_notification(save_time_of_down):
        await bot.send_message(message.chat.id, f"Вы увeрены, что легли в {save_time_of_down}?",
                               reply_markup=confirmation_kb_scenario)
        await ClientFMS.ui_down_state.set()
    else:
        await bot.send_message(message.chat.id, 'Введен неверный формат!')
        await command_rise(message, state)


async def command_confirmation(message: types.Message, state: FSMContext):
    user = await User.get(message.from_user.id)
    if message.text == '/Да':
        async with state.proxy() as data:
            await user.add_state_change(StateChange.FALL_ASLEEP, data['down'])
            await user.add_state_change(StateChange.WAKE_UP, data['rise'])
            await graphs.send_graphs(message)

    elif message.text == '/Нет':
        await bot.send_message(message.chat.id, "Напишите время, во сколько вы легли.")
        await bot.send_message(message.chat.id, 'Формат: "часы:минуты"')
        await ClientFMS.ui_rise_state.set()







