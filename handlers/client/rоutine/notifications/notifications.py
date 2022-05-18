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
    delimiter = State()
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
    #with state.proxy() as data:
     #   data['user_state'] = message.text
    await bot.send_message(message.chat.id, "Вы уверены?", reply_markup=confirmation_kb_scenario)
    await RoutineFSM.delimiter.set()

async def delimiter_yes_no(message: types.Message): # delimiter
    if message.text == '/Yes':
        await RoutineFSM.push_data_base.set()
        print('Запушено') # прописать улет на бд
    else:
        await RoutineFSM.time_to_check.set()
        await command_five_sts(message.chat.id)

async def push_to_database(message: types.Message, state: FSMContext):
    await state.finish()

def routine_handlers(dp:Dispatcher):
    dp.register_message_handler(starter, commands=['notif'], state=None)
    dp.register_message_handler(command_are_you_sure, commands=['Просто_ужасно', 'Плохо', 'Пойдет', 'Хорошо', 'Отлично'], state=RoutineFSM.are_you_sure)
    dp.register_message_handler(delimiter_yes_no, commands=['No', 'Yes'], state=RoutineFSM.delimiter)
    dp.register_message_handler(push_to_database, state=RoutineFSM.delimiter)