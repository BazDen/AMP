from peewee import *
from modules.base import BaseModel


class TZ(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=50)
    utc = SmallIntegerField()

    class Meta:
        db_table = "tz"


async def list_tz():
    return list(TZ.select())


async def get_tz(id: int):
    return TZ.filter(TZ.id == id).first().name
