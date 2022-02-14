from peewee import *
from database import conn

class BaseModel(Model):
    class Meta:
        database = conn


