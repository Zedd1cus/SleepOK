from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from keyboards.client_kb import kb_settings, kb_advice, kb_back


kb_create_advice = KeyboardButton('/Создать')
kb_delete_advice = KeyboardButton('/Удалить')
kb_show_advices = KeyboardButton('/Показать')
kb_5_11_advices = KeyboardButton('/5:00-11:00', hour=7)
kb_11_15_advices = KeyboardButton('/11:00-15:00', hour=12)
kb_15_20_advices = KeyboardButton('/15:00-20:00', hour=16)
kb_20_5_advices = KeyboardButton('/20:00-5:00', hour=21)


admin_show_interface_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_show_interface_kb_scenario.row(kb_create_advice, kb_delete_advice).add(kb_back)

admin_ui_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_ui_kb_scenario.row(kb_settings)

admin_settings_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_settings_kb_scenario.row(kb_advice, kb_back)

admin_advice_interface_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_advice_interface_kb_scenario.row(kb_show_advices, kb_back)

admin_time_of_advices_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_time_of_advices_kb_scenario.row(kb_5_11_advices, kb_11_15_advices).\
    row(kb_15_20_advices, kb_20_5_advices).add(kb_back)

