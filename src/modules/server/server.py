from peewee import *
from modules.base import BaseModel


class SrvSettings(BaseModel):
    id = PrimaryKeyField(null=False)
    tz = SmallIntegerField()
    name = CharField(max_length=50)

    class Meta:
        db_table = "server_settings"


async def get_srv_tz():
    return SrvSettings.filter().first().tz


async def set_srv_tz(tz: int):
    s = SrvSettings.filter().first()
    s.tz = tz
    s.save()


async def get_srv_name():
    return SrvSettings.filter().first().name


async def set_srv_name(name: str):
    s = SrvSettings.filter().first()
    s.name = name
    s.save()


  
