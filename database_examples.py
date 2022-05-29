import asyncio
import datetime
import random
from typing import List

# Подключение классов для работы с базой
from database import connect
from database.user import User
from database.state_change import StateChange
from database.advice import Advice

# Рантайм для работы с async, не пригодится для написания функций
loop = asyncio.get_event_loop()


# Примеры
async def main():
    # Подключение к базе данных
    await connect.init()

    # print(await User.is_registered(1235))
    # Получение пользователя по Telegram ID
    user = await User.get(12345)
    print('Пользователь', user)

    # Назначение времени подъема
    await user.set_time_to_up(datetime.time.fromisoformat('06:00'))
    # Назначение времени сна
    await user.set_time_to_sleep(datetime.time.fromisoformat('22:00'))
    # Назначение времени уведомлений
    await user.set_notification_time([
        datetime.time.fromisoformat('10:00'),
        datetime.time.fromisoformat('16:00'),
        datetime.time.fromisoformat('20:00'),
    ])
    print('После изменений', user.notification_time)

    # Работа с отметками (настроением 1-5)
    # Получение всех отметок пользователя
    print('Отметки', await user.get_all_marks())

    # Добавление отметок
    await user.add_mark(3)
    await user.add_mark(4)
    await user.add_mark(5)
    print('После добавлений', await user.get_all_marks())

    # Получение и удаление последней метки
    mark = await user.get_last_mark()
    print('Последняя отметка', mark)
    if mark is not None:
        # Если отметка существует - удаляем
        await mark.delete()
    print('После удаления последней', await user.get_all_marks())

    # Добавление статусов (встал/лег)
    await user.add_state_change(StateChange.WAKE_UP)
    await user.add_state_change(StateChange.FALL_ASLEEP)
    print('Все статусы', await user.get_all_states())
    last_state = await user.get_last_state()
    print('Последний статус', last_state)
    await last_state.delete()
    print('Статусы после удаления последнего', await user.get_all_states())

    # # Работа с советами
    # print("Все советы", await Advice.get_all_advices())
    # await Advice.create(3, "Не ешь перед сном")
    # await Advice.create(5, "Не спи днем")
    # await Advice.create(5, "Больше занимайся спортом")
    # print("Все советы после добавлений", await Advice.get_all_advices())
    # print("Советы по mark=5", await Advice.get_advices_by_mark(5))
    #
    # # Отдельный пример
    # import random
    #
    # # получение советов по состоянию 3
    # advices = await Advice.get_advices_by_mark(3)
    #
    # # получение рандомного совета
    # advice = random.choice(advices)
    #
    # #  advice.uid - его ID
    # #  advice.advice - сам совет, str
    # #  advice.mark - состояние
    #
    # # удаление совета
    # await advice.delete()
    #
    # # либо можно удалить через ID
    # await Advice.delete_by_uid(advice.uid)


async def check_changes():
    await connect.init()

    # получение советов по состоянию 5 (отлично)
    # игнорируя время
    advices = await Advice.get_advices_by_mark(5)
    print(len(advices), random.choice(advices))

    # получение по состоянию 5 (отлично) и по текущему часу;
    # например, если сейчас 20:08, то будут получены советы
    # в которых указан час 20 (в доке указаны как 20:00-5:00)
    # и состояние 5
    advices = await Advice.get_advices_by_mark_and_hour(5)
    print(len(advices), random.choice(advices))

    # получение только по времени (игнорируется состояние)
    advices = await Advice.get_advices_by_hour()
    print(len(advices), random.choice(advices))


# Запуск async функции (примера)
loop.run_until_complete(check_changes())
