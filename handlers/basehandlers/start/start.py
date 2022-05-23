from aiogram import types
from src.create_bot import bot
from aiogram import Dispatcher
from keyboards.client_kb import verify_kb_scenario
from aiogram.dispatcher.filters.state import State, StatesGroup


class StartFMS(StatesGroup):
    start_state = State()


async def command_start(message: types.Message):
    await bot.send_message(message.chat.id, "What's up!", reply_markup=verify_kb_scenario)
    await StartFMS.start_state.set()


def start_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])



