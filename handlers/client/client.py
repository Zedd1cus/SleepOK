from aiogram import Dispatcher

# User interface moduls
from handlers.client.userinterface.help import help
from handlers.client.userinterface.risedown import rise, down
from handlers.client.userinterface.settings import settings
from handlers.client.userinterface.settings.reset import confirmation, reset

# User interface module
from handlers.client.clientscenario import client_states_scenario

# Start settings module
from handlers.client.settings import start_settings

# Routine module
from handlers.client.rоutine.notifications import notifications


# User interface handlers
def user_interface_handlers(dp: Dispatcher):
    # UI Settings
    dp.register_message_handler(settings.command_settings, commands=['settings'],
                                state=None)
    dp.register_message_handler(reset.command_reset, commands=['reset', 'back'],
                                state=client_states_scenario.ClientFMS.ui_settings_state)

    dp.register_message_handler(confirmation.command_confirmation, commands=['Yes', 'No'],
                                state=client_states_scenario.ClientFMS.ui_reset_state)

    # UI Help
    dp.register_message_handler(help.command_help, commands=['help'])

    # UI Rise or down
    dp.register_message_handler(rise.command_rise, commands=['rise'])
    dp.register_message_handler(down.command_down, commands=['down'])


# Routine handlers
def routine_handlers(dp:Dispatcher):
    dp.register_message_handler(notifications.starter, commands=['notif'], state=None)
    dp.register_message_handler(notifications.command_are_you_sure,
                                commands=['Плохо', 'Ниже_среднего', 'Средне', 'Выше_среднего', 'Отлично'],
                                state=notifications.RoutineFSM.are_you_sure)
    dp.register_message_handler(notifications.delimiter_yes_no, commands=['No', 'Yes'],
                                state=notifications.RoutineFSM.push_data_base)


# Start settings handlers
def start_settings_handlers(dp: Dispatcher):
    # Rise register handlers
    dp.register_message_handler(start_settings.command_rise, commands=['client'], state=None)
    dp.register_message_handler(start_settings.command_set_up_rise,
                                state=client_states_scenario.ClientFMS.settings_rise)
    dp.register_message_handler(start_settings.command_confirmation_rise, commands=['Yes', 'No'],
                                state=client_states_scenario.ClientFMS.settings_set_up_rise)

    # Sleep register handlers
    dp.register_message_handler(start_settings.command_set_up_sleep,
                                state=client_states_scenario.ClientFMS.settings_confirmation_rise)
    dp.register_message_handler(start_settings.command_confirmation_sleep, commands=['Yes', 'No'],
                                state=client_states_scenario.ClientFMS.settings_set_up_sleep)

    # Time of notification register handlers
    dp.register_message_handler(start_settings.command_set_up_time_of_notification,
                                state=client_states_scenario.ClientFMS.settings_confirmation_sleep)
    dp.register_message_handler(start_settings.command_confirmation_time_of_notification, commands=['Yes', 'No'],
                                state=client_states_scenario.ClientFMS.settings_set_up_time_of_notification)
