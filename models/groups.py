from peewee import *
from .base import BaseModel


class Groups(BaseModel):
    id = PrimaryKeyField(null=False)
    name = CharField(max_length=50)

    class Meta:
        db_table = "groups"


async def list_groups(status: int, group: int):
    if int(status) == 1:
        return list(Groups.select())
    else:
        return list(Groups.filter(Groups.id == int(group)))


async def group_edit(id: int, name: str):
    g = Groups.filter(Groups.id == id).first()
    g.name = name
    g.save()


def group_not_exist(name: str):
    if int(Groups.filter(Groups.name == name).count())==0:
        return True
    else:
        return False    

async def group_add(name: str):
    if group_not_exist(name):
        g = Groups(name=name)
        g.save()
        return g


async def group_remove(id: int):
    return Groups.delete().where(Groups.id == id).execute()

