from aiogram import types, Dispatcher
from src.create_bot import bot
from keyboards.client_kb import kb_client, new_kb_client


async def command_start(message: types.Message):
    await bot.send_message(message.chat.id, "What's up!", reply_markup=kb_client)


async def command_help(message: types.Message):
    await bot.send_message(message.chat.id, "This is help!", reply_markup=kb_client)


async def command_time(message: types.Message):
    await bot.send_message(message.chat.id, "This is time!", reply_markup=new_kb_client)

#
# async def command_notification(message: types.Message):
#     await bot.send_message(message.chat.id, "This is notification!")


async def command_graph(message: types.Message):
    await bot.send_message(message.chat.id, "This is graph!")


async def command_advice(message: types.Message):
    await bot.send_message(message.chat.id, "This is advice!")


async def command_restart(message: types.Message):
    await bot.send_message(message.chat.id, "This is restart!")


def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'])
    dp.register_message_handler(command_help, commands=['help'])
    dp.register_message_handler(command_time, commands=['time'])
    # dp.register_message_handler(command_notification, commands=['notification'])
    dp.register_message_handler(command_graph, commands=['graph'])
    dp.register_message_handler(command_advice, commands=['advice'])
    dp.register_message_handler(command_restart, commands=['restart'])

