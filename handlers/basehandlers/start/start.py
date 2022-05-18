from aiogram import types
from src.create_bot import bot
from aiogram import Dispatcher
from keyboards.client_kb import verify_kb_scenario


async def command_start(message: types.Message):
    await bot.send_message(message.chat.id, "What's up!", reply_markup=verify_kb_scenario)


def start_handler(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
