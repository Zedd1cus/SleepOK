from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

b1 = KeyboardButton('/time')
b2 = KeyboardButton('/notification')
b3 = KeyboardButton('/graph')
b4 = KeyboardButton('/advice')
b5 = KeyboardButton('/restart')

kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

new_kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

kb_client.row(b1, b2).row(b3, b4).add(b5)

new_kb_client.row(b5, b3)
