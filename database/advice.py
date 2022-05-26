from typing import List

from database.connect import get_poll
import datetime


class Advice:
    def __init__(self, uid: int, marks: List[int], hours: List[int], advice: str):
        self.advice: str = advice
        self.marks: List[int] = marks
        self.hours: List[int] = hours
        self.uid: int = uid

    def __str__(self):
        return f'Advice(UID:{self.uid}, Marks:{self.marks}, Hours:{self.hours} Advice:{self.advice})'

    __repr__ = __str__

    @staticmethod
    async def create(marks: List[int], hours: List[int], advice: str):
        await get_poll().execute('insert into advices (Marks, Hours, Advice) values ($1, $2, $3)', marks, hours, advice)

    async def delete(self):
        await Advice.delete_by_uid(self.uid)

    @staticmethod
    async def delete_by_uid(uid: int):
        await get_poll().execute('delete from advices where uid=$1', uid)

    @staticmethod
    async def get_all_advices() -> List['Advice']:
        sql = 'select UID, Marks, Hours, Advice from advices order by UID desc'
        advices = await get_poll().fetch(sql)

        result = []
        for advice in advices:
            result.append(Advice(*advice))
        return result

    @staticmethod
    async def get_advices_by_mark(mark: int) -> List['Advice']:
        sql = 'select UID, Marks, Hours, Advice from advices where $1 = ANY (Marks) order by UID desc'
        advices = await get_poll().fetch(sql, mark)

        result = []
        for advice in advices:
            result.append(Advice(*advice))
        return result

    @staticmethod
    async def get_advices_by_mark_and_hour(mark: int, hour: int = datetime.datetime.now().hour) -> List['Advice']:
        sql = 'select UID, Marks, Hours, Advice from advices where $1 = ANY (Marks) and $2 = ANY (Hours) order by UID desc'
        advices = await get_poll().fetch(sql, mark, hour)

        result = []
        for advice in advices:
            result.append(Advice(*advice))
        return result

    @staticmethod
    async def get_advices_by_hour(hour: int = datetime.datetime.now().hour) -> List['Advice']:
        sql = 'select UID, Marks, Hours, Advice from advices where $1 = ANY (Hours) order by UID desc'
        advices = await get_poll().fetch(sql, hour)

        result = []
        for advice in advices:
            result.append(Advice(*advice))
        return result
