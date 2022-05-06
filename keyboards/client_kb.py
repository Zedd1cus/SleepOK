from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_help = KeyboardButton('/help')
kb_rise = KeyboardButton('/rise')
kb_down = KeyboardButton('/down')
kb_settings = KeyboardButton('/settings')
kb_back = KeyboardButton('/back')
kb_reset = KeyboardButton('/reset')
kb_yes = KeyboardButton('/Yes')
kb_no = KeyboardButton('/No')
kb_advice = KeyboardButton('/advice')
kb_verify_client = KeyboardButton('/client')
kb_verify_admin = KeyboardButton('/admin')


ui_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
settings_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
confirmation_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
verify_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)


verify_kb_scenario.row(kb_verify_client, kb_verify_admin)

ui_kb_scenario.row(kb_rise, kb_down).row(kb_help, kb_settings)
settings_kb_scenario.row(kb_reset, kb_back)
confirmation_kb_scenario.row(kb_yes, kb_no)

admin_kb_scenario.add(kb_advice)




