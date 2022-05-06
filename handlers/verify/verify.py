from aiogram import Dispatcher
from handlers.verify.verifyclient import verify_client
from handlers.verify.verifyadmin import verify_admin


def verify_handlers(dp: Dispatcher):
    dp.register_message_handler(verify_client.command_verify_client, commands=['client'])
    dp.register_message_handler(verify_admin.command_verify_admin, commands=['admin'])

