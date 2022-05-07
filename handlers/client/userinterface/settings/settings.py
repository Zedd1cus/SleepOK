from aiogram import types
from src.create_bot import bot
from keyboards.client_kb import client_settings_kb_scenario
from handlers.client.clientscenario import client_states_scenario


async def command_settings(message: types.Message):
    await bot.send_message(message.chat.id, "This is settings!", reply_markup=client_settings_kb_scenario)
    await client_states_scenario.ClientFMS.ui_settings_state.set()

