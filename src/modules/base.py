from peewee import *
from config.database import db_connection


class BaseModel(Model):
    class Meta:
        database = db_connection
