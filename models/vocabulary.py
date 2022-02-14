from peewee import *
from .base import BaseModel


class Vocabulary(BaseModel):
    id = PrimaryKeyField(null=False)
    code = CharField(max_length=2)
    name = CharField()
    value = CharField()

    class Meta:
        db_table = "vocabulary"


async def get_labels(code: str):
    return { l.name: l.value for l in Vocabulary.select().filter(Vocabulary.code==code) }

