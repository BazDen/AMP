from peewee import *
from .base import BaseModel


class Lang(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=25)
    code = CharField(max_length=2)

    class Meta:
        db_table = "lang"


async def list_lang(skip: int = 0, limit: int = 100):
    return list(Lang.select().offset(skip).limit(limit))


async def get_lang(id: int):
    l = Lang.filter(Lang.id == id).first()
    if l == None:
        return 'en'
    else:     
        return l.code
