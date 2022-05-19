import types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram import Dispatcher, types
from src.create_bot import bot
from keyboards.client_kb import five_states_kb_scenario, confirmation_kb_scenario
from aiogram.dispatcher import FSMContext
from database import connect
from database.user import User
from database.state_change import StateChange
from database.advice import Advice
import time


class RoutineFSM(StatesGroup):
    time_to_check = State()
    are_you_sure = State()
    push_data_base = State()


async def starter(message:types.Message):
    await hand_time(message.chat.id, ['21:00'])


async def hand_time(chat_id, times):
    if True:
        await RoutineFSM.time_to_check.set()
        await command_five_sts(chat_id)


async def command_five_sts(chat_id): #  time_to_check
    await bot.send_message(chat_id, "Как ваши ощущения?", reply_markup=five_states_kb_scenario)
    await RoutineFSM.next()


async def command_are_you_sure(message: types.Message, state:FSMContext): # are_you_sure
    async with state.proxy() as data:
        data['user_state'] = message.text
    await bot.send_message(message.chat.id, "Вы уверены?", reply_markup=confirmation_kb_scenario)
    await RoutineFSM.push_data_base.set()


async def delimiter_yes_no(message: types.Message, state): # push_data_base
    if message.text == '/Yes':
        await push_to_database(message, state)
    else:
        await RoutineFSM.time_to_check.set()
        await command_five_sts(message.chat.id)


async def push_to_database(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data_to_push = data['user_state']
    print(data_to_push)
    print('Запушено')  # прописать улет на бд
    await state.finish()