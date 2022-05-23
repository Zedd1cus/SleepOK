from aiogram import Dispatcher

# Start state module
from handlers.basehandlers.start.start import StartFMS

# Admin admin moduls
from handlers.admin.adminscenario.admin_states_scenario import AdminFSM, command_admin
from handlers.admin.admininterface.settings import settings
from handlers.admin.admininterface.settings.advice import advice


# Admin admin handlers
def settings_handlers(dp: Dispatcher):
    # Admin start
    dp.register_message_handler(command_admin, commands=['admin'], state=StartFMS.start_state)

    # Admin settings
    dp.register_message_handler(settings.command_settings, commands=['settings'],
                                state=AdminFSM.settings_state)

    dp.register_message_handler(advice.command_advice, commands=['advice', 'back'],
                                state=AdminFSM.advice_state)

    dp.register_message_handler(advice.command_advice_interface, commands=['show', 'back'],
                                state=AdminFSM.advice_interface_state)

    dp.register_message_handler(advice.command_mark_interface, commands=['Плохо', 'Ниже_среднего', 'Средне',
                                'Выше_среднего', 'Отлично'], state=AdminFSM.show_interface_state)

    dp.register_message_handler(advice.perform_action, commands=['delete', 'create'],
                                state=AdminFSM.action_interface_state)

    dp.register_message_handler(advice.confirmation_for_delete, state=AdminFSM.delete_interface_state)

    dp.register_message_handler(advice.delete, commands=['Yes', 'No'],
                                state=AdminFSM.confirmation_for_delete_state)

    dp.register_message_handler(advice.confirmation_for_create, state=AdminFSM.create_interface_state)

    dp.register_message_handler(advice.create, commands=['Yes', 'No'],
                                state=AdminFSM.confirmation_for_create_state)
