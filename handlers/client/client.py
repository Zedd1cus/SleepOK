from aiogram import Dispatcher

# User interface moduls
from handlers.client.userinterface.start import start
from handlers.client.userinterface.help import help
from handlers.client.userinterface.risedown import rise, down
from handlers.client.userinterface.settings import settings
from handlers.client.userinterface.settings.back import back
from handlers.client.userinterface.settings.reset import confirmation, reset


# User interface handlers
def user_interface_handlers(dp: Dispatcher):
    dp.register_message_handler(start.command_start, commands=['start'])
    dp.register_message_handler(help.command_help, commands=['help'])
    dp.register_message_handler(settings.command_settings, commands=['settings'])
    dp.register_message_handler(reset.command_reset, commands=['reset'])
    dp.register_message_handler(back.command_back, commands=['back'])
    dp.register_message_handler(confirmation.command_confirmation, commands=['Yes', 'No'])
    dp.register_message_handler(rise.command_rise, commands=['rise'])
    dp.register_message_handler(down.command_down, commands=['down'])

