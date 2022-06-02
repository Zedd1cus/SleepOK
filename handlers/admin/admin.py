from aiogram import Dispatcher

# Start state module
# from handlers.basehandlers.start.start import StartFMS

# Admin admin moduls
from handlers.admin.adminscenario.admin_states_scenario import AdminFSM, command_admin
from handlers.admin.admininterface.settings import settings
from handlers.admin.admininterface.settings.advice import advice


# Admin admin handlers
def settings_handlers(dp: Dispatcher):
    # Admin start
    dp.register_message_handler(command_admin, commands=['admin'])

    # Admin settings
    dp.register_message_handler(settings.command_settings, commands=['Настройки'],
                                state=AdminFSM.settings_state)

    dp.register_message_handler(advice.command_advice, commands=['Советы', 'Назад'],
                                state=AdminFSM.advice_state)

    dp.register_message_handler(advice.command_advice_interface, commands=['Показать', 'Назад'],
                                state=AdminFSM.advice_interface_state)

    dp.register_message_handler(advice.command_mark_interface, commands=['Плохо', 'Ниже_среднего', 'Средне',
                                'Выше_среднего', 'Отлично', 'Назад'], state=AdminFSM.show_interface_state)

    dp.register_message_handler(advice.command_time_interface, commands=['5:00-11:00', '11:00-15:00',
                                                                         '15:00-20:00', '20:00-5:00', 'Назад'],
                                state=AdminFSM.action_interface_state)

    dp.register_message_handler(advice.perform_action, commands=['Удалить', 'Создать', 'Назад'],
                                state=AdminFSM.time_interface_state)

    dp.register_message_handler(advice.confirmation_for_delete, state=AdminFSM.delete_interface_state)

    dp.register_message_handler(advice.delete, commands=['Да', 'Нет'],
                                state=AdminFSM.confirmation_for_delete_state)

    dp.register_message_handler(advice.confirmation_for_create, state=AdminFSM.create_interface_state)

    dp.register_message_handler(advice.create, commands=['Да', 'Нет'],
                                state=AdminFSM.confirmation_for_create_state)
