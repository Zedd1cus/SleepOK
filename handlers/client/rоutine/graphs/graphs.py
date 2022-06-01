from handlers.client.rоutine.graphs.moodgraph import graph1
from handlers.client.rоutine.graphs.timesgraph import graph2
from handlers.client.userinterface import user_interface
from database.user import User
from src.create_bot import bot
from aiogram import types
import os
import datetime

async def save_graphs(week_states:list, week_times:list):
    fig1, ax1 = await graph1.states_graph(mean_values=week_states)
    fig2, ax2 = await graph2.times_graph(week_times[0], week_times[1], week_times[2])
    await del_graph_local()
    fig1.savefig('temp_graph.png') # удалять сразу после отправки пользователю
    fig2.savefig('temp_graph2.png') # удалять сразу после отправки пользователю


async def send_graphs(message: types.Message): # эту ф-цию вызывать после того, как user нажал на /rise и подтвердил
                                                # и не
    tid = message.from_user.id
    if datetime.datetime.today().weekday() == 0:
        await bot.send_message(tid, 'Новая порция графов!')
        user = await User.get(tid)
        sr_states_7days = await user.get_last_7_marks()
        st_changes = await user.get_last_7_state_changes()
        rises = []
        downs = []
        for state_ch in st_changes:
            if state_ch.state == 1:
                rises.append(f'{state_ch.timestamp.hour}:{state_ch.timestamp.minute}')
            if state_ch.state == 0:
                downs.append(f'{state_ch.timestamp.hour}:{state_ch.timestamp.minute}')
        tms = [rises, downs, [user.time_to_up, user.time_to_sleep]]
        await save_graphs(sr_states_7days, tms)
        file1 = open('temp_graph.png', 'rb')
        file2 = open('temp_graph2.png', 'rb')
        await bot.send_photo(tid, photo=file1)
        await bot.send_photo(tid, photo=file2)
        file1.close()
        file2.close()
        await del_graph_local()
    await user_interface.command_base_ui(message.chat.id)


async def del_graph_local():
    if 'temp_graph.png' in os.listdir():
        os.remove('temp_graph.png')
    if 'temp_graph2.png' in os.listdir():
        os.remove('temp_graph2.png')


if __name__ == '__main__':
    pass