from peewee import *
from .base import BaseModel


class Webusers(BaseModel):
    id = PrimaryKeyField(null=False)
    fullname = CharField(max_length=100)
    username = CharField(max_length=50)
    password_sha256 = CharField(max_length=100)
    status = SmallIntegerField()
    tz = SmallIntegerField()
    layout = SmallIntegerField()
    group = SmallIntegerField()
    lang = CharField(max_length=2)

    class Meta:
        db_table = "webusers"


def list_users(skip: int = 0, limit: int = 100):
     return list(Webusers.select().offset(skip).limit(limit))

def get_user(username: str):
     return Webusers.filter(Webusers.username == username).first()


def get_layout(user: int, path: str):
    webuser = Webusers.filter(Webusers.id == user).first()
    return int(webuser.layout)


async def set_layout(user: int, layout: int, path: str):
    webuser = Webusers.filter(Webusers.id == user).first()
    webuser.layout = layout
    webuser.save()
    
def user_not_exist(username: str):
    if int(Webusers.filter(Webusers.username == username).count())==0:
        return True
    else:
        return False   

async def user_add(
    username: str, fullname: str, password: str, u_status: int, group: int, tz: int, lang:int
):
    if user_not_exist(username):
        u = Webusers(
            username=username,
            fullname=fullname,
            password_sha256=password,
            status=u_status,
            group=group,
            tz=tz,
            lang = lang,
            layout=3,
        )
        u.save()
        return u


async def user_edit(
    id: int,
    username: str,
    fullname: str,
    u_status: int,
    group: int,
    tz: int,
    userstatus: int,
    lang: int
):
    u = Webusers.filter(Webusers.id == id).first()
    if int(userstatus) == 1:
        u.username = username
        u.status = u_status
        u.group = group
    u.fullname = fullname
    u.tz = tz
    u.lang = lang
    u.save()


async def user_change_password(id: int, password: str):
    u = Webusers.filter(Webusers.id == id).first()
    u.password_sha256 = password
    u.save()


async def user_remove(id: int):
    return Webusers.delete().where(Webusers.id == id).execute()


