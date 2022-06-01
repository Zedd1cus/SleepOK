from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import five_states_kb_scenario, confirmation_kb_scenario, kb_st_bad, kb_st_below_average, \
        kb_st_average, kb_st_above_average, kb_st_excellent
from aiogram.dispatcher import FSMContext
from time import sleep
from database import connect
from database.user import User
from database.state_change import StateChange
from database.advice import Advice
import datetime

state_buttons = []
state_buttons.append(kb_st_bad)
state_buttons.append(kb_st_below_average)
state_buttons.append(kb_st_average)
state_buttons.append(kb_st_above_average)
state_buttons.append(kb_st_excellent)

class RoutineFSM(StatesGroup):
    time_to_check = State()
    are_you_sure = State()
    push_data_base = State()

async def starter(message: types.Message):
    # await connect.init()
    # global user
    global notif_times
    # user = await User.get(message.from_user.id)
    # notif_times = user.notification_time
    #notif_times = [datetime.time(16, 14), datetime.time(16, 16)]
    await hand_time(message.from_user.id) #, notif_times)

async def hand_time(chat_id, times=None):
    times = [datetime.time(16, 53), datetime.time(16, 54)]
    while True:
        sleep(60)
        dt = datetime.datetime.now()
        if datetime.time(dt.hour, dt.minute) in times:
            await RoutineFSM.time_to_check.set()
            await command_five_sts(chat_id)
            break



async def command_five_sts(chat_id): #  time_to_check
    await bot.send_message(chat_id, "Как ваши ощущения?", reply_markup=five_states_kb_scenario)
    await RoutineFSM.next()


async def command_are_you_sure(message: types.Message, state:FSMContext): # are_you_sure
    async with state.proxy() as data:
        data['user_state'] = message.text
    await bot.send_message(message.from_user.id, "Вы уверены?", reply_markup=confirmation_kb_scenario)
    await RoutineFSM.push_data_base.set()


async def delimiter_yes_no(message: types.Message, state): # push_data_base
    if message.text == '/Yes':
        await push_to_database(message.from_user.id, state)
    else:
        await RoutineFSM.time_to_check.set()
        await command_five_sts(message.from_user.id)

def get_state_id(message: types.Message) -> int:
    for button in state_buttons:
        if message.text == button.text:
            return int(button['index'])


async def push_to_database(chat_id, state: FSMContext):
    async with state.proxy() as data:
        stated = data['user_state']
    # mark = get_state_id(stated)
    # await user.add_mark(mark)
    # print(f'Пользователь {user.tid} отправил состояние {mark} на бд')
    await state.finish()
    await hand_time(chat_id) #, notif_times)

print(datetime.time())