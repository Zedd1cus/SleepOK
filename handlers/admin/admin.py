from aiogram import Dispatcher

# Admin admin moduls
from handlers.admin.adminscenario import admin_states_scenario
from handlers.admin.admininterface.settings import settings
from handlers.admin.admininterface.settings.advice import advice


# Admin admin handlers
def settings_handlers(dp: Dispatcher):
    # Admin start
    dp.register_message_handler(admin_states_scenario.command_admin, commands=['admin'], state=None)

    # Admin settings
    dp.register_message_handler(settings.command_settings, commands=['settings'],
                                state=admin_states_scenario.AdminFSM.settings_state)
    dp.register_message_handler(advice.command_advice, commands=['advice', 'back'],
                                state=admin_states_scenario.AdminFSM.advice_state)
