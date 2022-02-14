from peewee import *
from .base import BaseModel
from playhouse.shortcuts import model_to_dict

class Status(BaseModel):
    id = PrimaryKeyField(null=False)
    ru = CharField(max_length=25)
    en = CharField(max_length=25)

    class Meta:
        db_table = "status"


def list_status(code: str):
    status_list = list(Status.select())
    status_list = [model_to_dict(l) for l in status_list]
    for l in status_list:
        if code == 'ru':
            l['name'] = l['ru']
        elif code == 'en':
            l['name'] = l['en']
        else:
            l['name'] = l['en']        
    return status_list

