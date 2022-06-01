from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


kb_help = KeyboardButton('/help')
kb_rise = KeyboardButton('/rise')
kb_settings = KeyboardButton('/settings')
kb_back = KeyboardButton('/back')
kb_reset = KeyboardButton('/reset')
kb_yes = KeyboardButton('/Yes')
kb_no = KeyboardButton('/No')
kb_advice = KeyboardButton('/advice')
kb_st_bad = KeyboardButton('/Плохо', index=1)
kb_st_below_average = KeyboardButton('/Ниже_среднего', index=2)
kb_st_average = KeyboardButton('/Средне', index=3)
kb_st_above_average = KeyboardButton('/Выше_среднего', index=4)
kb_st_excellent = KeyboardButton('/Отлично', index=5)
kb_time_of_rise = KeyboardButton('/time_of_first_rise')
kb_time_of_down = KeyboardButton('/time_of_first_down')
kb_time_of_notification = KeyboardButton('/time_of_notification')


confirmation_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
confirmation_kb_scenario.row(kb_yes, kb_no)

# verify_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# verify_kb_scenario.row(kb_verify_client, kb_verify_admin)

client_ui_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_ui_kb_scenario.add(kb_rise).row(kb_help, kb_settings)

client_settings_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_settings_kb_scenario.row(kb_reset, kb_back)

five_states_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
five_states_kb_scenario.row(kb_st_excellent, kb_st_bad).\
    row(kb_st_above_average, kb_st_average, kb_st_below_average)

client_reset_kb_scenario = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
client_reset_kb_scenario.row(kb_time_of_rise, kb_time_of_down).row(kb_time_of_notification, kb_back)


