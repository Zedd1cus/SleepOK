from datetime import datetime, timedelta
from typing import List, Optional

from database.connect import get_poll


class Mark:
    def __init__(self, uid: int, tid: int, value: int, timestamp: datetime):
        self.timestamp: datetime = timestamp
        self.value: int = value
        self.tid: int = tid
        self.uid: int = uid

    def __str__(self):
        return f'Mark(UID:{self.uid}, TID:{self.tid}, Value:{self.value}, Timestamp:{self.timestamp})'

    __repr__ = __str__

    @staticmethod
    async def get_all_by_tid(tid) -> List['Mark']:
        sql = 'select UID, TID, Value, Timestamp from marks where TID=$1 order by UID desc'
        marks = await get_poll().fetch(sql, tid)

        result = []
        for mark in marks:
            result.append(Mark(*mark))
        return result

    @staticmethod
    async def get_last_by_tid(tid) -> Optional['Mark']:
        sql = 'select UID, TID, Value, Timestamp from marks where TID=$1 order by UID desc limit 1'
        marks = await get_poll().fetch(sql, tid)

        if len(marks) == 1:
            return Mark(*marks[0])
        return None

    @staticmethod
    async def get_by_tid(tid, start: datetime, end: datetime):
        sql = 'select UID, TID, Value, Timestamp from marks where TID=$1 and timestamp > $2 and timestamp < $3 order by UID desc'
        marks = await get_poll().fetch(sql, tid, start, end)

        result = []
        for mark in marks:
            result.append(Mark(*mark))
        return result

    async def delete(self):
        await get_poll().execute('delete from marks where uid=$1', self.uid)

