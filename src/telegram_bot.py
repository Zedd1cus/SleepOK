from aiogram import executor
from create_bot import dp

from handlers.client import client
from handlers.admin import admin
from handlers.basehandlers.start import start


async def one_startup(_) -> None:
    print('Bot online...')


start.start_handler(dp)

client.user_interface_handlers(dp)
client.start_settings_handlers(dp)
client.routine_handlers(dp)

admin.settings_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=one_startup)
