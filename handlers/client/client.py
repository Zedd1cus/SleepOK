from aiogram import Dispatcher

# User interface moduls
from handlers.basehandlers.start import start
from handlers.client.userinterface.help import help
from handlers.client.userinterface.risedown import rise, down
from handlers.client.userinterface.settings import settings
from handlers.client.userinterface.settings.reset import confirmation, reset

from handlers.client.clientscenario import client_states_scenario


# User interface handlers
def user_interface_handlers(dp: Dispatcher):
    # UI Start
    dp.register_message_handler(client_states_scenario.command_client, commands=['client'])

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



