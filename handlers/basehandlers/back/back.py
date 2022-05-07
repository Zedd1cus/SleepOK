from aiogram import types
from src.create_bot import bot
from aiogram.types import ReplyKeyboardMarkup


async def command_back(message: types.Message, markup: ReplyKeyboardMarkup):
    await bot.send_message(message.chat.id, "This is back!", reply_markup=markup)

