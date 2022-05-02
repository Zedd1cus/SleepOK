from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

token = '5379205499:AAHdOdZQEB3nLpYAAg8GmAfw1291lz-CXZ8'
bot = Bot(token)
dp = Dispatcher(bot, storage=storage)

