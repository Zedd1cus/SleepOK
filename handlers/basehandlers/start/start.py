from aiogram import types

from handlers.client.settings import start_settings
from src.create_bot import bot
from aiogram import Dispatcher
from aiogram.dispatcher.filters.state import State, StatesGroup

from database import connect
from database.user import User
from database.state_change import StateChange
from database.advice import Advice
from database.user import User
from handlers.client.userinterface import user_interface


# class StartFMS(StatesGroup):
#     start_state = State()
#
#
# async def command_start(message: types.Message):
#     # Сюда добавить проверку на id админа, если да, то часть админа,
#     # если нет, то часть клиента
#     # is_user_in = await User.is_registered(message.from_user.id)
#     if True: # is_user_in
#         await start_settings.command_rise(message)
#         await StartFMS.start_state.set()
#
#
# def start_handler(dp: Dispatcher):
#     dp.register_message_handler(command_start, commands=['start'])
