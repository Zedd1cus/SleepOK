from aiogram import executor
from create_bot import dp

from handlers.client import client
from handlers.admin import admin
from handlers.basehandlers.start import start
from handlers.client.settings import start_settings
from handlers.client.userinterface.settings import settings
from handlers.client.rоutine.notifications.notification_new import handle_all_players


async def one_startup(_) -> None:
    print('Bot online...')


async def started(_):
    await handle_all_players()

start.start_handler(dp)
client.start_settings_handlers(dp)
client.new_routine_handlers(dp)
client.user_interface_handlers(dp)
client.base_ui_handlers(dp)

admin.settings_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=started)

