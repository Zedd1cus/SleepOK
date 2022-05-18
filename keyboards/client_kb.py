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
kb_st_shut_up = KeyboardButton('/Просто_ужасно')
kb_st_bad = KeyboardButton('/Плохо')
kb_st_normal = KeyboardButton('/Пойдет')
kb_st_good = KeyboardButton('/Хорошо')
kb_st_super = KeyboardButton('/Отлично')

confirmation_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
confirmation_kb_scenario.row(kb_yes, kb_no)


verify_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
verify_kb_scenario.row(kb_verify_client, kb_verify_admin)


client_ui_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_ui_kb_scenario.row(kb_rise, kb_down).row(kb_help, kb_settings)

client_settings_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_settings_kb_scenario.row(kb_reset, kb_back)

client_rise_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_rise_kb_scenario.row(kb_rise, kb_back)

client_down_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_down_kb_scenario.row(kb_down, kb_back)

admin_ui_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_ui_kb_scenario.row(kb_settings)

admin_settings_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
admin_settings_kb_scenario.row(kb_advice, kb_back)

five_states_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
five_states_kb_scenario.row(kb_st_super).row(kb_st_good).row(kb_st_normal).row(kb_st_bad).row(kb_st_shut_up)




