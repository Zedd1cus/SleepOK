from typing import List

from database.connect import get_conn


class Advice:
    def __init__(self, uid: int, mark: int, advice: str):
        self.advice: str = advice
        self.mark: int = mark
        self.uid: int = uid

    def __str__(self):
        return f'Advice(UID:{self.uid}, Mark:{self.mark}, Advice:{self.advice})'

    __repr__ = __str__

    @staticmethod
    async def create(mark: int, advice: str):
        await get_conn().execute('insert into advices (Mark, Advice) values ($1, $2)', mark, advice)

    async def delete(self):
        await Advice.delete_by_uid(self.uid)

    @staticmethod
    async def delete_by_uid(uid: int):
        await get_conn().execute('delete from advices where uid=$1', uid)

    @staticmethod
    async def get_all_advices() -> List['Advice']:
        sql = 'select UID, Mark, Advice from advices order by UID desc'
        advices = await get_conn().fetch(sql)

        result = []
        for advice in advices:
            result.append(Advice(*advice))
        return result

    @staticmethod
    async def get_advices_by_mark(mark: int) -> List['Advice']:
        sql = 'select UID, Mark, Advice from advices where Mark=$1 order by UID desc'
        advices = await get_conn().fetch(sql, mark)

        result = []
        for advice in advices:
            result.append(Advice(*advice))
        return result
