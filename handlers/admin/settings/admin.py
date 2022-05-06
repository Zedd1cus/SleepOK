from aiogram import Dispatcher

# Admin settings moduls
from handlers.admin.settings.advice import advice


# Admin settings handlers
def settings_handlers(dp: Dispatcher):
    dp.register_message_handler(advice.command_advice, commands=['advice'])

