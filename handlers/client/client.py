from aiogram import Dispatcher

# Client start module
# from handlers.basehandlers.start.start import StartFMS

# User interface moduls
from handlers.client.userinterface.help import help
from handlers.client.userinterface.risedown import rise, down
from handlers.client.userinterface.settings import settings

# ClientFSM import
from handlers.client.clientscenario.client_states_scenario import ClientFMS

# Start settings module
from handlers.client.settings import start_settings

# Routine module
from handlers.client.rоutine.notifications import notifications, notification_new
from handlers.client.rоutine.graphs import graphs

# UI module
from handlers.client.userinterface.settings import settings
from handlers.client.userinterface.user_interface import command_base_ui, command_user_selection


# Base UI handlers
def base_ui_handlers(dp: Dispatcher):
    dp.register_message_handler(command_base_ui, state=None)
    dp.register_message_handler(command_user_selection,
                                commands=['help', 'rise', 'settings'],
                                state=ClientFMS.selection_state)


# User interface handlers
def user_interface_handlers(dp: Dispatcher):
    # UI Settings
    dp.register_message_handler(settings.command_settings, commands=['settings'],
                                state=None)
    dp.register_message_handler(settings.command_reset, commands=['reset', 'back'],
                                state=ClientFMS.ui_settings_state)

    dp.register_message_handler(settings.command_confirmation_reset, commands=['Yes', 'No'],
                                state=ClientFMS.ui_reset_state)

    # Rise and down
    dp.register_message_handler(rise.command_down, state=ClientFMS.ui_rise_state)
    dp.register_message_handler(rise.command_confirmation, commands=['Yes', 'No'],
                                state=ClientFMS.ui_down_state)
    dp.register_message_handler(rise.rise_agree, commands=['Yes', 'No'],  state=ClientFMS.rise_agree)
    dp.register_message_handler(rise.rise_changed, state=ClientFMS.rise_changed)
    dp.register_message_handler(rise.rise_changed_agree, commands=['Yes', 'No'], state=ClientFMS.rise_changed_agree)

# Routine handlers
def routine_handlers(dp:Dispatcher):
    dp.register_message_handler(graphs.send_graphs_test, commands=['graph'])
    dp.register_message_handler(notifications.send_notification,
                                commands=['notif'])
    dp.register_message_handler(notifications.command_are_you_sure,
                                commands=['Плохо', 'Ниже_среднего', 'Средне', 'Выше_среднего', 'Отлично'],
                                state=notifications.RoutineFSM.check_state)
    dp.register_message_handler(notifications.delimiter_yes_no,
                                commands=['Yes', 'No'],
                                state=notifications.RoutineFSM.push_data_base)


# Start settings handlers
def start_settings_handlers(dp: Dispatcher):
    # Rise register handlers
    dp.register_message_handler(start_settings.command_rise, commands=['start'])
    dp.register_message_handler(start_settings.command_set_up_rise,
                                state=ClientFMS.settings_rise)
    dp.register_message_handler(start_settings.command_confirmation_rise, commands=['Yes', 'No'],
                                state=ClientFMS.settings_set_up_rise)

    # Sleep register handlers
    dp.register_message_handler(start_settings.command_set_up_sleep,
                                state=ClientFMS.settings_confirmation_rise)
    dp.register_message_handler(start_settings.command_confirmation_sleep, commands=['Yes', 'No'],
                                state=ClientFMS.settings_set_up_sleep)

    # Time of notification register handlers
    dp.register_message_handler(start_settings.command_set_up_time_of_notification,
                                state=ClientFMS.settings_confirmation_sleep)
    dp.register_message_handler(start_settings.command_confirmation_time_of_notification, commands=['Yes', 'No'],
                                state=ClientFMS.settings_set_up_time_of_notification)


def new_routine_handlers(dp: Dispatcher):
    dp.register_message_handler(notification_new.send_notification,
                                state=notification_new.RoutineFSM.check_state)
    dp.register_message_handler(notification_new.command_are_you_sure,
                                commands=['Плохо', 'Ниже_среднего', 'Средне', 'Выше_среднего', 'Отлично'],
                                state=notification_new.RoutineFSM.check_state)
    dp.register_message_handler(notification_new.delimiter_yes_no,
                                commands=['Yes', 'No'],
                                state=notification_new.RoutineFSM.push_data_base)
