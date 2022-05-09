from datetime import datetime
from typing import List, Optional

from database.connect import get_conn


class StateChange:
    # статусы пользователя
    FALL_ASLEEP = 0
    WAKE_UP = 1

    def __init__(self, uid: int, tid: int, state: int, timestamp: datetime):
        self.timestamp: datetime = timestamp
        self.state: int = state
        self.tid: int = tid
        self.uid: int = uid

    def __str__(self):
        return f'StateChange(UID:{self.uid}, TID:{self.tid}, State:{self.state}, Timestamp:{self.timestamp})'

    __repr__ = __str__

    @staticmethod
    async def get_all_by_tid(tid) -> List['StateChange']:
        sql = 'select UID, TID, State, Timestamp from state_changes where TID=$1 order by UID desc'
        states = await get_conn().fetch(sql, tid)

        result = []
        for state in states:
            result.append(StateChange(*state))
        return result

    @staticmethod
    async def get_last_by_tid(tid) -> Optional['StateChange']:
        sql = 'select UID, TID, State, Timestamp from state_changes where TID=$1 order by UID desc limit 1'
        states = await get_conn().fetch(sql, tid)

        if len(states) == 1:
            return StateChange(*states[0])
        return None

    async def delete(self):
        await get_conn().execute('delete from state_changes where uid=$1', self.uid)