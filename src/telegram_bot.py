from aiogram import executor
from create_bot import dp

from handlers.verify import verify
from handlers.client import client
from handlers.admin.settings import admin


async def one_startup(_) -> None:
    print('Bot online...')


verify.verify_handlers(dp)
client.user_interface_handlers(dp)
admin.settings_handlers(dp)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=one_startup)