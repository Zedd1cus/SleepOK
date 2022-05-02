from aiogram import Dispatcher
from handlers.admin import notification
from handlers.admin import time
from handlers.admin import graph
from handlers.admin import advice


def notification_register_handlers(dp: Dispatcher):
    dp.register_message_handler(notification.command_notification_start, commands=['notification'], state=None)
    dp.register_message_handler(notification.set_state_1, state=notification.NotificationFSM.state_1)
    dp.register_message_handler(notification.set_state_2, state=notification.NotificationFSM.state_2)
    dp.register_message_handler(notification.set_state_3, state=notification.NotificationFSM.state_3)


def time_register_handlers(dp: Dispatcher):
    pass
