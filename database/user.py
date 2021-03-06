from datetime import datetime, time, timedelta
from typing import List, Optional

from database.connect import get_poll
from database.mark import Mark
from database.state_change import StateChange


class User:
    def __init__(self, tid, time_to_up, time_to_sleep, notification_time, node, created_date):
        self.created_date: datetime = created_date
        self.node: int = node
        self.notification_time: List[time] = notification_time
        self.time_to_sleep: Optional[time] = time_to_sleep
        self.time_to_up: Optional[time] = time_to_up
        self.tid: int = tid

    def __str__(self):
        return f'User(TID:{self.tid}, Up:{self.time_to_up}, Sleep:{self.time_to_sleep},' \
               f' Notifications:{self.notification_time}, Node:{self.node}, Created:{self.created_date})'

    __repr__ = __str__

    async def set_time_to_up(self, time_to_up: time):
        self.time_to_up = time_to_up
        await get_poll().execute('update users set TimeToUP=$1 where TID=$2', self.time_to_up, self.tid)

    async def set_time_to_sleep(self, time_to_sleep: time):
        self.time_to_sleep = time_to_sleep
        await get_poll().execute('update users set TimeToSleep=$1 where TID=$2', self.time_to_sleep, self.tid)

    async def set_node(self, node: int):
        self.node = node
        await get_poll().execute('update users set Node=$1 where TID=$2', self.node, self.tid)

    async def set_notification_time(self, notification_time: List[time]):
        self.notification_time = notification_time
        await get_poll().execute('update users set NotificationTime=$1 where TID=$2', self.notification_time, self.tid)

    async def add_mark(self, mark: int):
        await get_poll().execute('insert into marks (TID, Value) values ($1, $2)', self.tid, mark)

    async def add_state_change(self, state: int, timestamp: datetime = datetime.now()):
        await get_poll().execute('insert into state_changes (TID, State, Timestamp) values ($1, $2, $3)', self.tid, state, timestamp)

    async def get_last_mark(self) -> Optional[Mark]:
        return await Mark.get_last_by_tid(self.tid)

    async def get_all_marks(self) -> List[Mark]:
        return await Mark.get_all_by_tid(self.tid)

    async def get_all_states(self) -> List[StateChange]:
        return await StateChange.get_all_by_tid(self.tid)

    async def get_last_state(self) -> Optional[StateChange]:
        return await StateChange.get_last_by_tid(self.tid)

    @staticmethod
    async def create(tid: int) -> 'User':
        await get_poll().execute('insert into users (TID) values ($1)', tid)
        return await User.get(tid)

    @staticmethod
    async def get(tid: int) -> 'User':
        sql = 'select TID, TimeToUP, TimeToSleep, NotificationTime, Node, CreatedDate from users where TID=$1'
        values = await get_poll().fetch(sql, tid)
        # ???????? ???????????????????????? ?????? ?? ????????, ?????????????? ????????????
        if len(values) == 0:
            return await User.create(tid)

        # # ???????? ????????, ???????????????????? ???????????? ????????????????????????
        return User(*values[0])

    @staticmethod
    async def is_registered(tid: int) -> bool:
        sql = 'select TID, TimeToUP, TimeToSleep, NotificationTime, Node, CreatedDate from users where TID=$1'
        values = await get_poll().fetch(sql, tid)
        # ???????? ???????????????????????? ?????? ?? ????????, ?????????????? ????????????
        if len(values) == 0:
            return False

        # # ???????? ????????, ???????????????????? ???????????? ????????????????????????
        return True

    @staticmethod
    async def get_all_users() -> List['User']:
        sql = 'select TID, TimeToUP, TimeToSleep, NotificationTime, Node, CreatedDate from users'
        users = await get_poll().fetch(sql)

        # # ???????? ????????, ???????????????????? ???????????? ????????????????????????
        result = []
        for user in users:
            result.append(User(*user))
        return result

    async def get_last_7_marks(self) -> List[float]:
        """ ???????????????????? ???????????? ???? 7 float - ?????? ?????????????? ?????????????????? ???? ?????????????????? 7 ????????, ???? ?????????????? ?????????????????????? """
        n = datetime.now()
        end = datetime.replace(n, n.year, n.month, n.day, 0, 0, 0, 0)
        start = end - timedelta(days=7)
        marks = await Mark.get_by_tid(self.tid, start, end)

        counter = [[0, 0] for _ in range(7)]
        for day in range(7):
            for mark in marks:
                if (start + timedelta(days=day)) < mark.timestamp < (start + timedelta(days=day + 1)):
                    counter[day][0] += mark.value
                    counter[day][1] += 1

        result = []
        for day in range(7):
            if counter[day][1] == 0:
                result.append(0)
            else:
                result.append(counter[day][0] / counter[day][1])
        return result

    async def get_last_7_state_changes(self) -> List[List[Optional[StateChange]]]:
        """
        ???????????????????? ???????????? StateChange (??????????/??????) ???? ?????????????????? 7 ????????, ???? ?????????????? ?????????????????????? ?? ????????:
        [
            [StateChange(??????????), StateChange(??????)],
            ... (?????????? 7 ????????)
        ]

        ???????? ???????????????????????? ???? ??????????????????, ???????????? StateChange ?????????? None
        """
        n = datetime.now()
        end = datetime.replace(n, n.year, n.month, n.day, 5, 0, 0, 0)
        start = end - timedelta(days=7)
        states = await StateChange.get_by_tid(self.tid, start, end)

        result = [[None, None] for _ in range(7)]
        for day in range(7):
            for state in states:
                if (start + timedelta(days=day)) < state.timestamp < (start + timedelta(days=day + 1)):
                    if state.state == StateChange.WAKE_UP:
                        result[day][0] = state
                    else:
                        result[day][1] = state
        return result
