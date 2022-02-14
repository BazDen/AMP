from peewee import *
from .base import BaseModel
from models.tz import *


class SrvSettings(BaseModel):
    id = PrimaryKeyField(null=False)
    tz = SmallIntegerField()

    class Meta:
        db_table = "server_settings"


async def get_srv_tz():
    return SrvSettings.filter().first().tz


async def set_srv_tz(tz: int):
    s = SrvSettings.filter().first()
    s.tz = tz
    s.save()
  
