import asyncio
import datetime
import random
from aiogram.dispatcher.filters.state import StatesGroup, State
from src.create_bot import bot
from aiogram import types
from keyboards.client_kb import five_states_kb_scenario, confirmation_kb_scenario, kb_st_bad, kb_st_below_average, \
        kb_st_average, kb_st_above_average, kb_st_excellent
from database import connect
from aiogram.dispatcher import FSMContext
from database.user import User
from handlers.client.userinterface import user_interface
from database.advice import Advice

state_buttons = [kb_st_bad, kb_st_below_average, kb_st_average, kb_st_above_average, kb_st_excellent]

class RoutineFSM(StatesGroup):
    check_state = State()
    push_data_base = State()


async def send_notification(tid):
    await bot.send_message(tid, "Как ваши ощущения?", reply_markup=five_states_kb_scenario)


def get_sleep_time(notification_time) -> int:
    n = datetime.datetime.now()

    min_timedelta = None
    for time in notification_time:
        notificate = n.replace(n.year, n.month, n.day, time.hour, time.minute, 0, 0)
        if notificate < n:
            notificate += datetime.timedelta(days=1)

        if min_timedelta is None or notificate - n < min_timedelta:
            min_timedelta = notificate - n
    return min_timedelta.seconds


async def command_are_you_sure(message: types.Message, state:FSMContext): # check_state
    async with state.proxy() as data:
        data['user_state'] = message.text
    await bot.send_message(message.chat.id, "Вы уверены?", reply_markup=confirmation_kb_scenario)
    await RoutineFSM.push_data_base.set()


async def delimiter_yes_no(message: types.Message, state: FSMContext): # push_data_base
    if message.text == '/Yes':
        await push_to_database(message.from_user.id, state)
    else:
        await RoutineFSM.check_state.set()
        await send_notification(message.from_user.id)


async def push_to_database(tid, state: FSMContext):
    async with state.proxy() as data:
        stated = data['user_state']
    mark = get_state_id(stated)
    user = await User.get(tid)
    await user.add_mark(mark)
    print(f'Пользователь {user.tid} отправил состояние {mark} на бд')
    # получение советов по состоянию 3
    advices = await Advice.get_advices_by_mark_and_hour(mark)
    # # получение рандомного совета
    advice = random.choice(advices)
    await bot.send_message(tid, advice.advice)
    asyncio.create_task(handle_player(tid))
    await user_interface.command_base_ui(tid)



def get_state_id(message: types.Message) -> int:
    for button in state_buttons:
        if message.text == button.text:
            return int(button['index'])


async def handle_player(tid: int): # для польз вне бд asyncio.create_task(handle_player(user.tid))
    while True:
        player = await User.get(tid)
        print('handle_player', get_sleep_time(player.notification_time))
        await asyncio.sleep(get_sleep_time(player.notification_time))
        player_updated = await User.get(tid)
        if player.notification_time != player_updated.notification_time:
            continue
        await RoutineFSM.check_state.set()
        await send_notification(tid)


async def handle_all_players(): # должна запускаться с самим ботом on_startup
    await connect.init()
    for user in await User.get_all_users():
        if user.tid != 653694622:
            asyncio.create_task(handle_player(user.tid))
            asyncio.create_task(user_interface.command_base_ui(user.tid))
        else:
            await bot.send_message(653694622, 'Напиши /admin')


if __name__ == '__main__':
    pass