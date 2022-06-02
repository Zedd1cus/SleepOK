import datetime
import random
from aiogram.dispatcher.filters.state import StatesGroup, State
from src.create_bot import bot
from aiogram import types
from keyboards.client_kb import five_states_kb_scenario, confirmation_kb_scenario, kb_st_bad, kb_st_below_average, \
        kb_st_average, kb_st_above_average, kb_st_excellent
from aiogram.dispatcher import FSMContext
from database.advice import Advice

state_buttons = [kb_st_bad, kb_st_below_average, kb_st_average, kb_st_above_average, kb_st_excellent]

class RoutineFSM(StatesGroup):
    check_state = State()
    push_data_base = State()

async def send_notification(message: types.Message):
    await bot.send_message(message.from_user.id, "Как ваши ощущения?", reply_markup=five_states_kb_scenario)
    await RoutineFSM.check_state.set()


def get_sleep_time(notification_time: list[datetime.time]) -> float:
    at_the_moment = datetime.datetime.now()
    first_dif = None
    for time in notification_time:
        first = (time.hour * 60 + time.minute) * 60
        second = (at_the_moment.hour * 60 + at_the_moment.minute) * 60
        dif = first - second
        if first_dif is None:
            first_dif = dif
        if dif >= 0:
            return dif
    return abs(first_dif)


async def command_are_you_sure(message: types.Message, state:FSMContext): # check_state
    async with state.proxy() as data:
        data['user_state'] = message.text
    await bot.send_message(message.chat.id, "Вы уверены?", reply_markup=confirmation_kb_scenario)
    await RoutineFSM.push_data_base.set()


async def delimiter_yes_no(message: types.Message, state: FSMContext): # push_data_base
    if message.text == '/Да':
        await push_to_database(message.chat.id, state)
    else:
        await RoutineFSM.check_state.set()
        await send_notification(message.from_user.id)


async def push_to_database(tid, state: FSMContext):
    async with state.proxy() as data:
        stated = data['user_state']
    mark = get_state_id(stated)
    print(f'Пользователь user отправил состояние {mark} на бд')
    # получение советов по состоянию 3
    advices = await Advice.get_advices_by_mark_and_hour(mark)
    # # получение рандомного совета
    advice = random.choice(advices)
    await bot.send_message(tid, advice.advice)
    await state.finish()

def get_state_id(text) -> int:
    for button in state_buttons:
        if text == button.text:
            return int(button['index'])


if __name__ == '__main__':
    pass