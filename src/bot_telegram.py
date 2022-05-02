from aiogram import executor
from create_bot import dp

from handlers.client import client
from handlers.admin import admin
from handlers.other import other


async def one_startup(_):
    print('Bot online...')


client.register_handlers_client(dp)

admin.notification_register_handlers(dp)
admin.time_register_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=one_startup)